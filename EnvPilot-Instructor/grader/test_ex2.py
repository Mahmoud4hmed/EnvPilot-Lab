import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from lab.models import Environment, Event
from lab.queries import environment_rows
from lab.serializers import EnvironmentSerializer
pytestmark = pytest.mark.django_db


def test_constant_query_growth(domain):
    for i in range(70):
        env = Environment.objects.create(project=domain['p'], name=f'scale-{i}', status='ready' if i % 2 else 'pending')
        Event.objects.create(environment=env, message=f'old-{i}')
        Event.objects.create(environment=env, message=f'latest-{i}')
    counts = []
    for size in [5, 20, 60]:
        with CaptureQueriesContext(connection) as captured:
            result = EnvironmentSerializer(environment_rows(domain['a'].id)[:size], many=True).data
        assert len(result) == size
        assert all(r['latest_event'].startswith('latest-') for r in result)
        counts.append(len(captured))
    assert max(counts) - min(counts) <= 2, f'Query growth with row count: {counts}'
    assert max(counts) <= 12, f'Unexpected fixed overhead: {counts}'


def test_filter_order_pagination_and_boundaries(domain, client_for):
    for i in range(30):
        Environment.objects.create(project=domain['p'], name=f'page-{i}', status='ready')
    client = client_for('owner')
    url = f"/api/environments/?organization={domain['a'].id}&status=ready&page_size=5"
    first = client.get(url).data
    second = client.get(url + '&page=2').data
    assert first['count'] == 30
    assert len(first['results']) == len(second['results']) == 5
    ids = [row['id'] for row in first['results'] + second['results']]
    assert ids == sorted(ids, reverse=True) and len(set(ids)) == 10
    assert all(row['organization'] == domain['a'].id and row['status'] == 'ready' for row in first['results'] + second['results'])
    assert client.get(url + '&page=999').data['results'] == []
