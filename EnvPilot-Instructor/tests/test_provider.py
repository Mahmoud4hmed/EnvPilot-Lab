from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import pytest
import requests


@pytest.fixture
def provider(tmp_path):
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    env={**os.environ,'PORT':str(port),'PROVIDER_DB':str(tmp_path/'provider.sqlite3')}
    source=Path(__file__).resolve().parents[2]/'EnvPilot-Lab'/'provider'/'server.py'
    process=subprocess.Popen([sys.executable,str(source)],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    url=f'http://127.0.0.1:{port}'
    try:
        for _ in range(100):
            try:
                requests.get(url+'/health',timeout=.2).raise_for_status();break
            except requests.RequestException:
                if process.poll() is not None:raise AssertionError('Provider process did not start')
                time.sleep(.05)
        else:raise AssertionError('Provider health deadline')
        yield url
    finally:
        process.terminate();process.wait(timeout=5)


def post(url,key,scenario='success',name='demo',timeout=2):
    return requests.post(url+'/resources',headers={'Idempotency-Key':key},json={'name':name,'scenario':scenario},timeout=timeout)


def test_provider_parallel_idempotency_and_conflict(provider):
    with ThreadPoolExecutor(max_workers=8) as pool:
        responses=list(pool.map(lambda _:post(provider,'1:provision:same'),range(8)))
    assert all(r.status_code in [200,201] for r in responses)
    assert len({r.json()['id'] for r in responses})==1
    assert post(provider,'1:provision:same',name='changed').status_code==409
    assert post(provider,'2:provision:same').status_code==201
    assert len(requests.get(provider+'/resources').json())==2


def test_transient_before_creation_and_permanent(provider):
    assert post(provider,'transient','transient').status_code==503
    assert requests.get(provider+'/by-key/transient').status_code==404
    assert post(provider,'transient','transient').status_code==201
    assert post(provider,'permanent','permanent').status_code==422
    assert requests.get(provider+'/by-key/permanent').status_code==404


def test_lost_response_is_reconcilable(provider):
    with pytest.raises(requests.Timeout):post(provider,'lost','lost_response',timeout=.1)
    resource=requests.get(provider+'/by-key/lost').json()
    assert resource['id']
    assert post(provider,'lost','lost_response').json()==resource
    assert len(requests.get(provider+'/resources').json())==1
