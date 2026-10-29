"""HTTP dispatch regressions, independent of intentional exercise defects."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from lab.models import Environment, Membership, Operation, Organization, Project

pytestmark = pytest.mark.django_db


@pytest.fixture
def account():
    user = get_user_model().objects.create_user(username='protocol-user', password='ProtocolPass123!')
    org = Organization.objects.create(name='Protocol team')
    Membership.objects.create(user=user, organization=org, role='owner')
    project = Project.objects.create(organization=org, name='Protocol project')
    env = Environment.objects.create(project=project, name='protocol-env')
    operation = Operation.objects.create(organization=org, environment=env, key='protocol', fingerprint='protocol')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.create(user=user).key)
    return client, org, project, env, operation


def read_paths(account):
    _, org, _, env, operation = account
    return ['/api/me/', f'/api/projects/?organization={org.id}',
            f'/api/environments/?organization={org.id}', f'/api/environments/{env.id}/',
            f'/api/operations/{operation.id}/']


def test_get_head_options_and_rejected_methods(account):
    client, *_ = account
    for path in read_paths(account):
        get = client.get(path)
        assert get.status_code == 200
        assert client.head(path).status_code == 200
        options = client.options(path)
        assert options.status_code == 200
        assert {'GET', 'HEAD', 'OPTIONS'} <= set(options['Allow'].split(', '))
        rejected = client.delete(path)
        assert rejected.status_code == 405
        assert rejected.data['error']['details']['detail'].code == 'method_not_allowed'


def test_product_endpoints_keep_token_authentication(account):
    anonymous = APIClient()
    invalid = APIClient()
    invalid.credentials(HTTP_AUTHORIZATION='Token invalid-protocol-token')
    for path in read_paths(account):
        for client in (anonymous, invalid):
            response = client.get(path)
            assert response.status_code == 401
            assert response['WWW-Authenticate'] == 'Token'
            assert response.data['error']['code'] == 'unauthenticated'


@pytest.mark.parametrize('format', ['json', 'multipart'])
def test_password_login_preserves_input_formats_and_reuses_token(account, format):
    expected = Token.objects.get(user__username='protocol-user').key
    client = APIClient()
    response = client.post('/api/login/', {'username': 'protocol-user', 'password': 'ProtocolPass123!'}, format=format)
    assert response.status_code == 200
    assert response.data == {'token': expected}
    assert response['Content-Type'] == 'application/json'
    assert client.post('/api/login/', {'username': 'protocol-user', 'password': 'wrong'}, format=format).status_code == 400
    assert client.post('/api/login/', {}, format=format).status_code == 400
    assert client.get('/api/login/').status_code == 405
    assert client.options('/api/login/').status_code == 200
    assert client.get('/api/login/', HTTP_ACCEPT='text/html').status_code == 406


def test_post_dispatch_validation_and_provision_response(account, monkeypatch):
    client, org, project, env, operation = account
    created = client.post('/api/environments/', {'project': project.id, 'name': 'protocol-new'})
    assert created.status_code == 201
    assert created.data['status'] == 'pending' and created.data['provider_id'] == ''
    assert client.post('/api/environments/', {}).status_code == 400
    path = f'/api/environments/{env.id}/provision/'
    assert client.get(path).status_code == 405
    assert client.post(path, {}, HTTP_IDEMPOTENCY_KEY='').status_code == 400
    assert client.post(path, {'scenario': 'unknown'}, HTTP_IDEMPOTENCY_KEY='valid').status_code == 400
    monkeypatch.setattr('lab.views.start_provision', lambda *args: (operation, True))
    response = client.post(path, {'scenario': 'success'}, HTTP_IDEMPOTENCY_KEY='valid')
    assert response.status_code == 202 and response.data['id'] == operation.id
    monkeypatch.setattr('lab.views.ask', lambda *args: {'answer': 'protocol', 'citations': [], 'tool': None, 'fallback': True})
    response = client.post('/api/assistant/', {'organization': org.id, 'question': 'example'})
    assert response.status_code == 200 and response.data['answer'] == 'protocol'
    assert client.post('/api/assistant/', {'organization': org.id, 'question': []}).status_code == 400
    assert client.get('/api/assistant/').status_code == 405


def test_demo_session_methods_and_auth_override(settings):
    settings.LAB_DEMO_ROLE_SWITCH = False
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token deliberately-invalid')
    assert client.post('/api/demo-session/', {'role': 'owner'}).status_code == 404
    assert client.get('/api/demo-session/').status_code == 405
    assert client.options('/api/demo-session/').status_code == 200
    settings.LAB_DEMO_ROLE_SWITCH = True
    response = client.post('/api/demo-session/', {'role': 'unknown'})
    assert response.status_code == 400 and response.data['error']['code'] == 'invalid'
