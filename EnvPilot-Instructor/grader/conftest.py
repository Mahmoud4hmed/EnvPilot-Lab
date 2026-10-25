import sys
import pytest
from django.contrib.auth import get_user_model
from lab.models import Organization, Membership, Project, Environment, Event, SupportDocument
from rest_framework.test import APIClient


@pytest.fixture
def domain(db):
    User = get_user_model()
    users = {name: User.objects.create_user(username=name) for name in ['owner', 'developer', 'viewer', 'foreign', 'dual', 'outsider']}
    a = Organization.objects.create(name='Grader Nile')
    b = Organization.objects.create(name='Grader Delta')
    for user, org, role in [('owner', a, 'owner'), ('developer', a, 'developer'), ('viewer', a, 'viewer'), ('foreign', b, 'owner'), ('dual', a, 'viewer'), ('dual', b, 'developer')]:
        Membership.objects.create(user=users[user], organization=org, role=role)
    p = Project.objects.create(organization=a, name='API')
    q = Project.objects.create(organization=b, name='Secret')
    env = Environment.objects.create(project=p, name='sandbox')
    other = Environment.objects.create(project=q, name='foreign')
    for obj in [env, other]:
        Event.objects.create(environment=obj, message='Created')
    return {'users': users, 'a': a, 'b': b, 'p': p, 'q': q, 'env': env, 'other': other}


@pytest.fixture
def client_for(domain):
    def make(name):
        client = APIClient()
        client.force_authenticate(domain['users'][name])
        return client
    return make
