import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APIClient

pytestmark=pytest.mark.django_db


@pytest.fixture
def demo(settings):
    settings.LAB_DEMO_ROLE_SWITCH=True
    call_command('seed')
    return APIClient()


def test_demo_role_switch_is_explicitly_enabled(demo,settings):
    settings.LAB_DEMO_ROLE_SWITCH=False
    assert demo.post('/api/demo-session/',{'role':'owner'}).status_code==404


@pytest.mark.parametrize('role',['owner','developer','viewer','other_owner','dual','outsider'])
def test_fixed_demo_roles_use_real_accounts(demo,role):
    response=demo.post('/api/demo-session/',{'role':role})
    assert response.status_code==200
    assert response.data['username']==role and response.data['token']
    demo.credentials(HTTP_AUTHORIZATION='Token '+response.data['token'])
    me=demo.get('/api/me/')
    assert me.status_code==200
    assert me.data['memberships']==response.data['memberships']
    if role=='outsider':assert me.data['memberships']==[]
    if role=='dual':assert len(me.data['memberships'])==2


def test_role_switch_rejects_unknown_or_arbitrary_accounts(demo):
    get_user_model().objects.create_user(username='custom-admin',is_superuser=True)
    for role in ['custom-admin','superuser','',None,{},['owner']]:
        assert demo.post('/api/demo-session/',{'role':role}).status_code==400


def test_viewer_keeps_server_permissions_and_switch_ignores_password_changes(demo):
    user=get_user_model().objects.get(username='viewer')
    user.set_password('ChangedLocalPassword!');user.save()
    response=demo.post('/api/demo-session/',{'role':'viewer'})
    demo.credentials(HTTP_AUTHORIZATION='Token '+response.data['token'])
    from lab.models import Environment
    org=response.data['memberships'][0]['organization']
    env=Environment.objects.filter(project__organization_id=org).first()
    assert demo.post(f'/api/environments/{env.id}/provision/',{},HTTP_IDEMPOTENCY_KEY='viewer-demo').status_code==403
    assert APIClient().get('/api/me/').status_code==401
