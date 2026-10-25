import pytest
from django.core.management import call_command
from rest_framework.test import APIClient
from lab.models import Environment, Membership


@pytest.mark.django_db
def test_seed_auth_and_normal_navigation():
    call_command('seed')
    before = Environment.objects.count()
    call_command('seed')
    assert Environment.objects.count() == before == 480
    client = APIClient()
    assert client.get('/health/').status_code == 200
    assert client.get('/api/me/').status_code == 401
    response = client.post('/api/login/', {'username': 'owner', 'password': 'LabPass123!'})
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])
    me = client.get('/api/me/')
    org_id = me.data['memberships'][0]['organization']
    assert client.get(f'/api/projects/?organization={org_id}').status_code == 200
    listing = client.get(f'/api/environments/?organization={org_id}')
    assert listing.status_code == 200 and len(listing.data['results']) == 20
    assert client.get('/api/environments/999999/').status_code == 404
    assert Membership.objects.count() == 6
