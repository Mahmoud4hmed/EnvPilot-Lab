import requests
from celery import shared_task
from django.conf import settings
from .models import Environment, Event, Operation


@shared_task(bind=True)
def provision(self, operation_id):
    op = Operation.objects.select_related('environment').get(pk=operation_id)
    op.status = 'running'
    op.attempts += 1
    op.save()
    Environment.objects.filter(pk=op.environment_id).update(status='provisioning')
    try:
        response = requests.post(settings.PROVIDER_URL + '/resources', json={'name': op.environment.name, 'scenario': op.scenario}, timeout=0.3)
        response.raise_for_status()
        resource = response.json()
    except requests.RequestException as exc:
        op.status = 'failed'
        op.error = type(exc).__name__
        op.save()
        Environment.objects.filter(pk=op.environment_id).update(status='failed')
        Event.objects.create(environment_id=op.environment_id, message='Provider call failed: ' + op.error)
        return
    Environment.objects.filter(pk=op.environment_id).update(status='ready', provider_id=resource['id'])
    op.status = 'succeeded'
    op.error = ''
    op.save()
    Event.objects.create(environment_id=op.environment_id, message='Environment ready')
