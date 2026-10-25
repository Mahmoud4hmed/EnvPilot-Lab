import pytest
from rest_framework.test import APIClient
from lab.models import Environment
pytestmark = pytest.mark.django_db


def test_authentication_required():
    client = APIClient()
    assert client.get('/api/environments/?organization=1').status_code == 401
    assert client.post('/api/environments/', {'project': 1, 'name': 'ok'}).status_code == 401


@pytest.mark.parametrize('user', ['owner', 'developer', 'viewer', 'dual'])
def test_members_can_read_own_organization(domain, client_for, user):
    response = client_for(user).get(f"/api/environments/?organization={domain['a'].id}")
    assert response.status_code == 200
    assert [row['id'] for row in response.data['results']] == [domain['env'].id]
    assert client_for(user).get(f"/api/environments/{domain['env'].id}/").status_code == 200


def test_foreign_list_denied(domain, client_for):
    response = client_for('owner').get(f"/api/environments/?organization={domain['b'].id}")
    assert response.status_code == 403
    assert response.data['error']['code'] == 'forbidden'


def test_foreign_detail_concealed(domain, client_for):
    assert client_for('owner').get(f"/api/environments/{domain['other'].id}/").status_code == 404
    assert client_for('outsider').get(f"/api/environments/{domain['env'].id}/").status_code == 404


@pytest.mark.parametrize('user', ['viewer', 'dual', 'outsider'])
def test_nonwriters_cannot_create(domain, client_for, user):
    before = Environment.objects.count()
    assert client_for(user).post('/api/environments/', {'project': domain['p'].id, 'name': 'new'}).status_code in [403, 404]
    assert Environment.objects.count() == before


def test_related_project_scope(domain, client_for):
    response = client_for('owner').post('/api/environments/', {'project': domain['q'].id, 'name': 'new'})
    assert response.status_code == 404


@pytest.mark.parametrize('name', ['', '  ', 'bad name', '../escape', 'valid\n', 'A'*65])
def test_invalid_names(domain, client_for, name):
    response = client_for('owner').post('/api/environments/', {'project': domain['p'].id, 'name': name})
    assert response.status_code == 400
    assert response.data['error']['code'] == 'invalid'


@pytest.mark.parametrize('user', ['owner', 'developer'])
def test_legitimate_write(domain, client_for, user):
    response = client_for(user).post('/api/environments/', {'project': domain['p'].id, 'name': 'demo-api-2'})
    assert response.status_code == 201
    assert response.data['status'] == 'pending' and response.data['provider_id'] == ''


def test_missing_and_bad_input(domain, client_for):
    client = client_for('owner')
    assert client.get('/api/environments/999999/').status_code == 404
    assert client.post('/api/environments/', {'project': 999999, 'name': 'valid'}).status_code == 404
    assert client.post('/api/environments/', {'project': 'bad'}).status_code == 400
    assert client.get('/api/environments/?organization=bad').status_code == 400
