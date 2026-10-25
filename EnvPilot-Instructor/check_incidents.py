import importlib.util
from pathlib import Path
import sys
import urllib.request

root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location('labcli', root / 'lab.py')
labcli = importlib.util.module_from_spec(spec); spec.loader.exec_module(labcli)
scenarios = labcli.active()
if not scenarios:
    print('TRAINING: Activate one incident, repair its durable configuration, then run check 4. Repeat for the second incident.')
    sys.exit(1)
failures = []
for scenario in scenarios:
    target = 'proxy' if scenario == 'proxy' else 'worker'
    code = labcli.compose(['up', '-d', '--no-deps', '--force-recreate', target])
    if code:
        sys.exit(2)
    if scenario == 'proxy':
        import time
        time.sleep(1)
        try:
            assert urllib.request.urlopen('http://localhost:8090/health/', timeout=5).status == 200
            print('PASS: proxy healthy after durable recreation')
        except Exception as exc:
            failures.append(str(exc)); print('FAIL:', exc)
    else:
        code = labcli.compose(['run', '--rm', '--no-deps', '-v', f'{root.parent / "EnvPilot-Instructor" / "grader"}:/grader:ro', '-e', 'PYTHONPATH=/app', 'api', 'python', '/grader/worker_roundtrip.py', '--smoke'])
        if code:
            failures.append('Accepted job did not complete through actual worker')
        else:
            print('PASS: accepted job completes after durable worker recreation')
sys.exit(1 if failures else 0)
