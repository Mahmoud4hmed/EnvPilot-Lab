import hashlib
import json
from django.db import transaction
from rest_framework.exceptions import APIException
from .models import Event, Operation


class Conflict(APIException):
    status_code = 409
    default_detail = 'Idempotency key conflicts with an existing request or environment state.'


def start_provision(environment, key, scenario):
    fingerprint = hashlib.sha256(json.dumps({'environment': environment.id, 'scenario': scenario}, sort_keys=True).encode()).hexdigest()
    org_id = environment.project.organization_id
    existing = Operation.objects.filter(organization_id=org_id, kind='provision', key=key).first()
    if existing:
        return existing, False
    if environment.status != 'pending':
        raise Conflict()
    with transaction.atomic():
        operation = Operation.objects.create(organization_id=org_id, environment=environment, key=key, fingerprint=fingerprint, scenario=scenario)
        Event.objects.create(environment=environment, message='Provision request accepted')
        from .tasks import provision
        transaction.on_commit(lambda: provision.delay(operation.id))
    return operation, True
