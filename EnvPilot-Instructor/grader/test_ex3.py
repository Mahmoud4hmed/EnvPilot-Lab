import threading
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
import pytest
from django.db import close_old_connections, connection
from lab.models import Environment, Operation
from lab.services import start_provision, Conflict
from rest_framework.test import APIClient
pytestmark = pytest.mark.django_db(transaction=True)


def test_replay_conflict_and_scope(domain):
    with patch('lab.tasks.provision.delay'):
        one, created = start_provision(domain['env'], 'replay', 'success')
        two, created2 = start_provision(domain['env'], 'replay', 'success')
        assert created and not created2 and one.id == two.id
        with pytest.raises(Conflict):
            start_provision(domain['env'], 'replay', 'lost_response')
        other, _ = start_provision(domain['other'], 'replay', 'success')
        assert other.id != one.id


@pytest.mark.postgres
def test_parallel_api_calls_share_one_operation(domain):
    assert connection.vendor == 'postgresql', 'INFRASTRUCTURE: PostgreSQL required; SQLite is not a concurrency substitute'
    barrier = threading.Barrier(8)
    user = domain['users']['owner']
    env_id = domain['env'].id
    def request(_):
        close_old_connections()
        client = APIClient()
        client.force_authenticate(user)
        barrier.wait(timeout=10)
        try:
            response = client.post(f'/api/environments/{env_id}/provision/', {'scenario': 'success'}, HTTP_IDEMPOTENCY_KEY='parallel')
            return response.status_code, response.data
        finally:
            close_old_connections()
    with patch('lab.tasks.provision.delay'), ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(request, range(8)))
    assert all(code in [200, 202] for code, _ in results), results
    assert len({body['id'] for _, body in results}) == 1
    assert Operation.objects.filter(key='parallel').count() == 1


def test_new_key_cannot_reprovision_ready_environment(domain):
    domain['env'].status = 'ready'; domain['env'].save()
    with pytest.raises(Conflict):
        start_provision(domain['env'], 'new', 'success')


def test_provision_authorization_and_validation(domain, client_for):
    path = f"/api/environments/{domain['env'].id}/provision/"
    assert client_for('viewer').post(path, {}).status_code == 403
    assert client_for('foreign').post(path, {}).status_code == 403
    assert client_for('owner').post(path, {}).status_code == 400
    assert client_for('owner').post(path, {'scenario':'invalid'}, HTTP_IDEMPOTENCY_KEY='k').status_code == 400
