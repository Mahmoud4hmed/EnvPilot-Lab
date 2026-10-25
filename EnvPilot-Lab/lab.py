#!/usr/bin/env python3
"""Portable stdlib-only lab entry point. Run from Windows or Linux/WSL2."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
STATE = ROOT / '.lab'
INSTRUCTOR = ROOT.parent / 'EnvPilot-Instructor'
_ENGINE_CHECKED = False
RESET_FILES = {
    '1': ['backend/lab/views.py', 'backend/lab/serializers.py'],
    '2': ['backend/lab/queries.py', 'backend/lab/serializers.py'],
    '3': ['backend/lab/services.py', 'backend/lab/tasks.py', 'backend/lab/models.py'],
    '4': ['infra/nginx.conf', 'infra/incidents/proxy.conf', 'infra/incidents/queue.yaml'],
    '5': ['frontend/components/Dashboard.tsx', 'frontend/lib/api.ts'],
    '6': ['ansible/playbook.yml', 'ansible/templates/agent.conf.j2'],
    '7': ['backend/lab/assistant.py'],
}


def invoke(args, cwd=ROOT, capture=False, timeout=900):
    result = subprocess.run([str(a) for a in args], cwd=cwd, text=True, encoding='utf-8', errors='replace', capture_output=capture, timeout=timeout)
    if capture:
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    return result.returncode


def active():
    path = STATE / 'incidents.json'
    return json.loads(path.read_text()) if path.exists() else []


def compose(args, capture=False, overlays=True):
    global _ENGINE_CHECKED
    if not _ENGINE_CHECKED:
        probe = subprocess.run(['docker', 'version', '--format', '{{.Server.Os}}'], capture_output=True, text=True, timeout=20)
        if probe.returncode or probe.stdout.strip() != 'linux':
            raise RuntimeError('Linux Docker Engine is unavailable. Open Docker Desktop, resolve its startup error, then run python lab.py doctor.')
        _ENGINE_CHECKED = True
    command = ['docker', 'compose', '-f', str(ROOT / 'compose.yaml')]
    if overlays:
        for scenario in active():
            command += ['-f', str(ROOT / 'infra' / 'incidents' / f'{scenario}.yaml')]
    return invoke(command + args, capture=capture)


def must(code):
    if code:
        raise RuntimeError(f'INFRASTRUCTURE command exited {code}; see evidence above.')


def doctor():
    errors = []
    print(f'Python {sys.version.split()[0]}; workspace {ROOT}')
    if not shutil.which('docker'):
        errors.append('Install Docker Desktop with WSL2 integration, or Docker Engine + Compose v2 on Linux.')
    else:
        for command in [['docker', 'version'], ['docker', 'compose', 'version']]:
            try:
                if invoke(command, capture=True, timeout=20):
                    errors.append('Start Docker Desktop / Linux Docker Engine, then rerun python lab.py doctor.')
            except subprocess.TimeoutExpired:
                errors.append('Docker Engine did not answer within 20s. Open Docker Desktop and resolve its startup error.')
    if not INSTRUCTOR.is_dir():
        errors.append(f'Keep sibling instructor materials at {INSTRUCTOR}; exercise checks/mock need this folder.')
    for port in [8090, 8091]:
        with socket.socket() as sock:
            try:
                sock.bind(('127.0.0.1', port))
            except OSError:
                print(f'Port {port} already in use (normal if this lab is running).')
    for error in dict.fromkeys(errors):
        print('ACTION:', error)
    print('Suggested Docker resources: 4 CPUs, 6 GB RAM; images need Internet only at first build.')
    return 2 if errors else 0


def up():
    STATE.mkdir(exist_ok=True)
    must(compose(['up', '-d', '--build', '--wait', 'db', 'redis', 'provider']))
    must(compose(['build', 'api', 'web']))
    must(compose(['run', '--rm', '--no-deps', 'api', 'python', 'manage.py', 'migrate', '--noinput']))
    must(compose(['run', '--rm', '--no-deps', 'api', 'python', 'manage.py', 'seed']))
    must(compose(['up', '-d', '--wait', '--wait-timeout', '180']))
    print('Open http://localhost:8090 — owner / LabPass123!')


def check(exercise):
    reports = STATE / 'reports'
    reports.mkdir(parents=True, exist_ok=True)
    mount = ['-v', f'{INSTRUCTOR / "grader"}:/grader:ro', '-v', f'{reports}:/reports']
    if exercise in ['smoke', '1', '2', '3', '7']:
        test = 'tests/test_smoke.py' if exercise == 'smoke' else f'/grader/test_ex{exercise}.py'
        (reports / f'ex{exercise}.xml').unlink(missing_ok=True)
        code = compose(['run', '--rm', '--no-deps', *mount, '-e', 'PYTHONPATH=/app', 'api', 'pytest', '-c', '/app/pytest.ini', test, f'--junitxml=/reports/ex{exercise}.xml'])
        if exercise == 'smoke' and code == 0:
            code = compose(['run', '--rm', '--no-deps', 'web', 'npm', 'run', 'test:smoke'])
            if code == 0:
                code = compose(['run', '--rm', '--no-deps', *mount, '-e', 'PYTHONPATH=/app', 'api', 'python', '/grader/worker_roundtrip.py', '--smoke'])
        if exercise == '3':
            (reports / 'worker.json').unlink(missing_ok=True)
            worker_code = compose(['run', '--rm', '--no-deps', *mount, '-e', 'PYTHONPATH=/app', '-e', 'WORKER_REPORT=/reports/worker.json', 'api', 'python', '/grader/worker_roundtrip.py'])
            code = 2 if 2 in [code, worker_code] else code or worker_code
    elif exercise == '5':
        (reports / 'ex5.xml').unlink(missing_ok=True)
        code = compose(['run', '--rm', '--no-deps', '-v', f'{reports}:/reports', 'web', 'npm', 'run', 'test:exercise', '--', '--reporter=default', '--reporter=junit', '--outputFile=/reports/ex5.xml'])
    elif exercise == '6':
        build_code = compose(['build', 'ansible'])
        code = 2 if build_code else compose(['run', '--rm', '--no-deps', 'ansible', 'python', 'verify.py'])
    elif exercise == '4':
        code = invoke([sys.executable, INSTRUCTOR / 'check_incidents.py', ROOT])
    else:
        raise ValueError('Choose smoke or 1..7')
    if exercise != 'smoke':
        report_code = invoke([sys.executable, INSTRUCTOR / 'report.py', exercise, reports, str(code)])
        if report_code == 2:
            code = 2
    if code == 2 or (exercise == 'smoke' and code):
        print('INFRASTRUCTURE FAILURE: inspect connection/build/import/collection evidence above; starter smoke must pass.')
    elif code:
        print('EXPECTED TRAINING FAILURE: unfinished behavior checks did not pass. See per-criterion evidence; fix infrastructure errors before grading.')
    else:
        print('PASS: executed checks. Manual explanation criteria remain in the rubric.')
    return code


def incident(action, scenario):
    scenarios = active()
    if action == 'start' and scenario not in scenarios:
        scenarios.append(scenario)
    if action == 'stop' and scenario in scenarios:
        scenarios.remove(scenario)
    STATE.mkdir(exist_ok=True)
    (STATE / 'incidents.json').write_text(json.dumps(scenarios))
    target = 'proxy' if scenario == 'proxy' else 'worker'
    must(compose(['up', '-d', '--no-deps', '--force-recreate', target]))
    print(f'{scenario}: {action}. Config persisted; source/notes/data preserved. Active: {scenarios}')


def reset(exercise, yes):
    files = RESET_FILES[exercise]
    print('CODE ONLY reset scope:\n' + '\n'.join(files))
    print('Shared files may contain work from another exercise. DB, notes, and test additions remain. Full current source files are backed up before replacing them.')
    if not yes:
        print(f'No changes made. Rerun: python lab.py reset {exercise} --yes')
        return 0
    baseline = STATE / 'starter.zip'
    if not baseline.exists():
        raise RuntimeError('Missing starter snapshot; no files changed.')
    backup = STATE / 'backups' / (dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.zip')
    backup.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(backup, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in files:
            path = ROOT / name
            if path.is_file():
                archive.write(path, name)
    with zipfile.ZipFile(baseline) as archive:
        for name in files:
            (ROOT / name).write_bytes(archive.read(name))
    print(f'Restored selected starter code; backup: {backup}. Restart api/worker after backend edits. Rerun migrations only if you changed schema; reset does not reverse learner migrations.')
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    for name in ['doctor', 'up', 'down', 'seed', 'e2e']:
        subs.add_parser(name)
    subs.add_parser('check').add_argument('exercise', choices=['smoke', *map(str, range(1, 8))])
    hint = subs.add_parser('hint'); hint.add_argument('exercise', choices=list(RESET_FILES)); hint.add_argument('level', choices=['1','2','3'])
    inc = subs.add_parser('incident'); inc.add_argument('action', choices=['start','stop']); inc.add_argument('scenario', choices=['proxy','queue'])
    res = subs.add_parser('reset'); res.add_argument('exercise', choices=list(RESET_FILES)); res.add_argument('--yes', action='store_true')
    exam = subs.add_parser('exam'); exam.add_argument('action', choices=['start','status','submit']);
    args = parser.parse_args()
    if args.command == 'doctor': return doctor()
    if args.command == 'up': up(); return 0
    if args.command == 'down': return compose(['down'])
    if args.command == 'seed': return compose(['exec','-T','api','python','manage.py','seed'])
    if args.command == 'check': return check(args.exercise)
    if args.command == 'e2e': return compose(['run','--rm','--build','browser-tests'])
    if args.command == 'hint':
        print((ROOT / 'hints' / args.exercise / f'{args.level}.md').read_text(encoding='utf-8')); return 0
    if args.command == 'incident': incident(args.action, args.scenario); return 0
    if args.command == 'reset': return reset(args.exercise, args.yes)
    if args.command == 'exam': return invoke([sys.executable, INSTRUCTOR / 'exam.py', args.action, '--lab-root', ROOT])


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (RuntimeError, FileNotFoundError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f'INFRASTRUCTURE: {exc}', file=sys.stderr)
        sys.exit(2)
