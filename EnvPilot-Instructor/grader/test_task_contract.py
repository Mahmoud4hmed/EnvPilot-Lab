"""Extra construction checks using real HTTP but synchronous task execution.
These supplement, and never replace, worker_roundtrip.py's actual-worker checks.
"""
import importlib.util
from pathlib import Path
from unittest.mock import patch
import pytest
import requests
from lab.services import start_provision
from lab.tasks import provision

spec=importlib.util.spec_from_file_location('provider_fixture',Path(__file__).resolve().parents[1]/'tests'/'test_provider.py')
provider_fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(provider_fixture)
provider=provider_fixture.provider


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('scenario',['success','transient','lost_response','permanent'])
def test_http_task_contract(domain,settings,provider,scenario):
    settings.PROVIDER_URL=provider
    with patch('lab.tasks.provision.delay'):
        op,_=start_provision(domain['env'],'http-task',scenario)
    provision.apply(args=[op.id],throw=False).get(propagate=True)
    op.refresh_from_db();domain['env'].refresh_from_db()
    assert op.status==('failed' if scenario=='permanent' else 'succeeded')
    assert 1<=op.attempts<=3
    if scenario=='permanent':
        assert op.error and domain['env'].status=='failed'
        assert requests.get(provider+'/resources').json()==[]
    else:
        assert domain['env'].status=='ready' and domain['env'].provider_id
        before=requests.get(provider+'/resources').json()
        provision.apply(args=[op.id],throw=False).get(propagate=True)
        assert requests.get(provider+'/resources').json()==before
