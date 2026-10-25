from concurrent.futures import ThreadPoolExecutor
import threading
import pytest
from django.contrib.auth import get_user_model
from django.db import close_old_connections, connection
from rest_framework.test import APIClient
from mockapp.models import Team, Member, Memo, Audit
pytestmark=pytest.mark.django_db(transaction=True)


@pytest.fixture
def data():
    teams=[Team.objects.create(name=name) for name in ['Nile','Delta']]
    users={}
    for name,team,role in [('owner',teams[0],'owner'),('viewer',teams[0],'viewer'),('foreign',teams[1],'owner')]:
        users[name]=get_user_model().objects.create_user(username=name)
        Member.objects.create(user=users[name],team=team,role=role)
    return users,Memo.objects.create(team=teams[0],title='Handover')


def client(user):
    result=APIClient();result.force_authenticate(user);return result


def test_archive_and_replay(data):
    users,memo=data;c=client(users['owner']);url=f'/api/memos/{memo.id}/archive/'
    first=c.post(url,{});second=c.post(url,{})
    assert first.status_code==second.status_code==200
    assert first.data['archived_at'] and first.data['archived_at']==second.data['archived_at']
    assert first.data['title']=='Handover' and first.data['id']==memo.id
    assert Audit.objects.filter(memo=memo,action='archived').count()==1


def test_parallel_archive(data):
    assert connection.vendor=='postgresql','INFRASTRUCTURE: PostgreSQL required for parallel archive'
    users,memo=data;barrier=threading.Barrier(4)
    def call(_):
        close_old_connections();c=client(users['owner']);barrier.wait(timeout=10)
        try:
            result=c.post(f'/api/memos/{memo.id}/archive/',{});return result.status_code,result.data
        finally:close_old_connections()
    with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(call,range(4)))
    assert all(code==200 for code,_ in results)
    assert len({str(body['archived_at']) for _,body in results})==1
    assert Audit.objects.filter(memo=memo,action='archived').count()==1


@pytest.mark.parametrize('name,expected',[('viewer',403),('foreign',404)])
def test_authorization(data,name,expected):
    users,memo=data
    assert client(users[name]).post(f'/api/memos/{memo.id}/archive/',{}).status_code==expected
    assert Audit.objects.count()==0


def test_anonymous(data):
    _,memo=data;assert APIClient().post(f'/api/memos/{memo.id}/archive/',{}).status_code==401


def test_missing(data):
    users,_=data;assert client(users['owner']).post('/api/memos/999999/archive/',{}).status_code==404


def test_existing_behavior(data):
    users,memo=data;c=client(users['owner'])
    assert c.get('/api/memos/').status_code==200
    assert c.patch(f'/api/memos/{memo.id}/',{'title':'Updated'}).status_code==200
    assert c.patch(f'/api/memos/{memo.id}/',{'title':''}).status_code==400
