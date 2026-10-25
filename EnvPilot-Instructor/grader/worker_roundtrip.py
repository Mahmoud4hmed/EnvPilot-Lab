"""Run against seeded *live* DB with actual worker; unique fixtures survive for diagnosis."""
import json
import os
import sys
import time
import uuid
from pathlib import Path
import requests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.conf import settings
from django.contrib.auth import get_user_model
from lab.models import Environment, Operation, Project
from lab.services import start_provision
from lab.tasks import provision


def wait(op, expected='succeeded'):
    deadline = time.monotonic() + 25
    while time.monotonic() < deadline:
        op.refresh_from_db()
        if op.status in ['succeeded', 'failed']:
            break
        time.sleep(.2)
    assert op.status == expected, f'operation {op.id}: {op.status}; {op.error}; worker must consume provision queue'
    return op


def run(scenarios, duplicate=True):
    results = []
    failures = []
    try:
        requests.get(settings.PROVIDER_URL + '/health', timeout=2).raise_for_status()
        from config.celery import app
        assert app.control.inspect(timeout=2).ping(), 'No Celery worker answered control ping'
        project = Project.objects.filter(organization__name='Team Alpha').first()
    except Exception as exc:
        print('INFRASTRUCTURE:', exc)
        sys.exit(2)
    assert project, 'INFRASTRUCTURE: run seed first'
    for scenario in scenarios:
        key = 'check-' + uuid.uuid4().hex
        env = Environment.objects.create(project=project, name=key)
        try:
            op, _ = start_provision(env, key, scenario)
            wait(op, 'failed' if scenario == 'permanent' else 'succeeded')
            env.refresh_from_db()
            assert env.status == ('failed' if scenario == 'permanent' else 'ready')
            if scenario == 'permanent':
                assert op.error and op.attempts <= 3
            else:
                assert env.provider_id
                # Parallel duplicate deliveries execute in two genuine worker processes.
                if duplicate:
                    before = len([r for r in requests.get(settings.PROVIDER_URL + '/resources', timeout=2).json() if r.get('name') == env.name])
                    assert before == 1, f'Expected one resource for {env.name}; got {before}'
                    jobs = [provision.delay(op.id) for _ in range(4)]
                    for job in jobs:
                        job.get(timeout=25)
                    after = len([r for r in requests.get(settings.PROVIDER_URL + '/resources', timeout=2).json() if r.get('name') == env.name])
                    assert before == after, f'duplicate remote effects: {before} -> {after}'
                assert op.attempts <= 3
            results.append({'scenario':scenario, 'operation':op.id, 'passed':True})
        except Exception as exc:
            failures.append(str(exc)); results.append({'scenario':scenario,'operation':locals().get('op').id if 'op' in locals() else None,'passed':False,'evidence':str(exc)})
    print(json.dumps(results, indent=2))
    if os.getenv('WORKER_REPORT'):
        Path(os.environ['WORKER_REPORT']).write_text(json.dumps(results, indent=2))
    if failures:
        sys.exit(1)


if __name__ == '__main__':
    run(['success'] if '--smoke' in sys.argv else ['success', 'transient', 'lost_response', 'permanent'], duplicate='--smoke' not in sys.argv)
