"""Deterministic remote side effects. Data persists independently of API transactions."""
import json
import os
import sqlite3
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote

DB = os.getenv('PROVIDER_DB', '/data/provider.sqlite3')
os.makedirs(os.path.dirname(os.path.abspath(DB)), exist_ok=True)
lock = threading.Lock()
with sqlite3.connect(DB) as db:
    db.executescript('CREATE TABLE IF NOT EXISTS resources (key TEXT PRIMARY KEY, id TEXT, payload TEXT); CREATE TABLE IF NOT EXISTS attempts (key TEXT PRIMARY KEY, n INTEGER);')


class Handler(BaseHTTPRequestHandler):
    def reply(self, code, body):
        raw = json.dumps(body).encode()
        try:
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass

    def do_GET(self):
        if self.path == '/health':
            return self.reply(200, {'status': 'ok'})
        with lock, sqlite3.connect(DB) as db:
            if self.path == '/resources':
                rows = db.execute('SELECT key,id,payload FROM resources ORDER BY key').fetchall()
                return self.reply(200, [{'key': k, 'id': i, **json.loads(p)} for k, i, p in rows])
            key = unquote(self.path.removeprefix('/by-key/'))
            row = db.execute('SELECT id FROM resources WHERE key=?', (key,)).fetchone()
        self.reply(200 if row else 404, {'id': row[0]} if row else {'error': 'not_found'})

    def do_POST(self):
        if self.path != '/resources':
            return self.reply(404, {'error': 'not_found'})
        try:
            body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', '0'))))
            scenario = body.get('scenario', 'success')
            if scenario not in ['success', 'transient', 'lost_response', 'permanent'] or not isinstance(body.get('name'), str):
                raise ValueError()
        except (ValueError, TypeError):
            return self.reply(400, {'error': 'invalid'})
        key = self.headers.get('Idempotency-Key') or str(uuid.uuid4())
        with lock, sqlite3.connect(DB) as db:
            row = db.execute('SELECT id,payload FROM resources WHERE key=?', (key,)).fetchone()
            if row:
                if json.loads(row[1]) != body:
                    return self.reply(409, {'error': 'key_conflict'})
                return self.reply(200, {'id': row[0]})
            db.execute('INSERT INTO attempts(key,n) VALUES(?,1) ON CONFLICT(key) DO UPDATE SET n=n+1', (key,))
            n = db.execute('SELECT n FROM attempts WHERE key=?', (key,)).fetchone()[0]
            if scenario == 'permanent' or (scenario == 'transient' and n == 1):
                code = 422 if scenario == 'permanent' else 503
                db.commit()
                return self.reply(code, {'error': 'capacity' if code == 503 else 'unsupported'})
            resource_id = 'vm-' + uuid.uuid5(uuid.NAMESPACE_URL, key).hex[:16]
            db.execute('INSERT INTO resources VALUES(?,?,?)', (key, resource_id, json.dumps(body)))
        if scenario == 'lost_response':
            time.sleep(0.8)
        self.reply(201, {'id': resource_id})


if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0', int(os.getenv('PORT', '9000'))), Handler).serve_forever()
