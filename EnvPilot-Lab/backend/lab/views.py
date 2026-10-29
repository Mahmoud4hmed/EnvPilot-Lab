from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, parser_classes, permission_classes, renderer_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Environment, Membership, Operation, Project
from .permissions import organization_for
from .queries import environment_rows
from .serializers import EnvironmentInput, EnvironmentSerializer, OperationSerializer, ProvisionInput
from .services import start_provision
from .assistant import ask


def health(request):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    return JsonResponse({'status': 'ok'})


@api_view(['POST'])
@permission_classes([])
@throttle_classes([])
@parser_classes([parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser])
@renderer_classes([renderers.JSONRenderer])
def login(request):
    view = request.parser_context['view']
    serializer = AuthTokenSerializer(data=request.data, context={
        'request': request, 'format': view.format_kwarg, 'view': view,
    })
    serializer.is_valid(raise_exception=True)
    token, _ = Token.objects.get_or_create(user=serializer.validated_data['user'])
    return Response({'token': token.key})


def positive_int(value, field):
    try:
        result = int(value)
        if result < 1:
            raise ValueError()
        return result
    except (TypeError, ValueError):
        raise ValidationError({field: 'Must be a positive integer.'})


@api_view(['GET', 'HEAD'])
def me(request):
    memberships = Membership.objects.filter(user=request.user).select_related('organization')
    return Response({'username': request.user.username, 'memberships': [{'organization': m.organization_id, 'name': m.organization.name, 'role': m.role} for m in memberships]})


@api_view(['GET', 'HEAD'])
def projects(request):
    org = organization_for(request.user, positive_int(request.query_params.get('organization'), 'organization'))
    return Response(list(Project.objects.filter(organization=org).values('id', 'name')))


@api_view(['GET', 'POST', 'HEAD'])
def environments(request):
    if request.method in ('GET', 'HEAD'):
        org_id = positive_int(request.query_params.get('organization'), 'organization')
        rows = environment_rows(org_id)
        status = request.query_params.get('status')
        if status:
            if status not in dict(Environment.STATES):
                raise ValidationError({'status': 'Unknown lifecycle state.'})
            rows = rows.filter(status=status)
        page = positive_int(request.query_params.get('page', 1), 'page')
        size = min(positive_int(request.query_params.get('page_size', 20), 'page_size'), 100)
        return Response({'count': rows.count(), 'results': EnvironmentSerializer(rows[(page-1)*size:page*size], many=True).data})
    body = EnvironmentInput(data=request.data)
    body.is_valid(raise_exception=True)
    project = get_object_or_404(Project, pk=body.validated_data['project'])
    env = Environment.objects.create(project=project, name=body.validated_data['name'])
    return Response(EnvironmentSerializer(env).data, status=201)


@api_view(['GET', 'HEAD'])
def environment_detail(request, pk):
    env = get_object_or_404(Environment, pk=pk)
    return Response(EnvironmentSerializer(env).data)


@api_view(['POST'])
def provision(request, pk):
    env = get_object_or_404(Environment.objects.select_related('project'), pk=pk)
    organization_for(request.user, env.project.organization_id, write=True)
    body = ProvisionInput(data=request.data)
    body.is_valid(raise_exception=True)
    key = request.headers.get('Idempotency-Key', '')
    if not key or len(key) > 80:
        raise ValidationError({'Idempotency-Key': 'Required; 1 to 80 characters.'})
    op, created = start_provision(env, key, body.validated_data['scenario'])
    return Response(OperationSerializer(op).data, status=202 if created else 200)


@api_view(['GET', 'HEAD'])
def operation_detail(request, pk):
    op = get_object_or_404(Operation, pk=pk)
    organization_for(request.user, op.organization_id)
    return Response(OperationSerializer(op).data)


@api_view(['POST'])
def assistant(request):
    org = organization_for(request.user, positive_int(request.data.get('organization'), 'organization'))
    question = request.data.get('question', '')
    scenario = request.data.get('scenario', 'normal')
    if not isinstance(question, str) or len(question) > 200 or scenario not in ['normal', 'timeout', 'malformed', 'tool', 'forbidden_tool', 'injection']:
        raise ValidationError({'question': 'Invalid question or deterministic scenario.'})
    return Response(ask(request.user, org, question, scenario))
