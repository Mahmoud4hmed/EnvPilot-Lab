import os
import pathlib
import subprocess
import sys
import re


def run(port):
    result = subprocess.run(['ansible-playbook', '-i', 'localhost,', '-c', 'local', 'playbook.yml', '-e', f'agent_port={port}'], text=True, capture_output=True)
    print(result.stdout)
    print(result.stderr)
    if result.returncode:
        sys.exit(2)
    return result.stdout


run(9100)
path = pathlib.Path('/fixture/envpilot/config/agent.conf')
assert path.is_file(), 'config/agent.conf must exist'
assert path.stat().st_mode & 0o777 == 0o640, 'configuration permissions must be 0640'
assert pathlib.Path('/fixture/envpilot/config').stat().st_mode & 0o777 == 0o750
assert pathlib.Path('/fixture/envpilot/logs').stat().st_mode & 0o777 == 0o750
assert path.read_text() == '# Managed by Ansible\nservice=envpilot-agent\nport=9100\n'
second = run(9100)
assert re.search(r'changed=0\b', second), 'unchanged second run must report zero changes'
run(9200)
assert 'port=9200\n' in path.read_text(), 'changed input must update configuration'
run(9100)
print('PASS: contents, modes, unchanged second run, changed input')
