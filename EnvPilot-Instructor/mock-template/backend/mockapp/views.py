from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, parser_classes, permission_classes, renderer_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Memo


def health(request):
    return JsonResponse({'status':'ok'})


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


def payload(memo):
    return {'id':memo.id,'title':memo.title,'archived_at':memo.archived_at}


def scoped(user, pk):
    return get_object_or_404(Memo, pk=pk, team=user.member.team)


@api_view(['GET', 'HEAD'])
def memos(request):
    return Response([payload(m) for m in Memo.objects.filter(team=request.user.member.team).order_by('id')])


@api_view(['PATCH'])
def memo_detail(request, pk):
    memo = scoped(request.user, pk)
    if request.user.member.role != 'owner':
        raise PermissionDenied()
    title = request.data.get('title')
    if not isinstance(title, str) or not title.strip() or len(title) > 60:
        raise ValidationError({'title':'Required nonblank string, max 60 chars.'})
    memo.title = title; memo.save(update_fields=['title'])
    return Response(payload(memo))


@api_view([])
def archive(request, pk):
    # New product request remains unimplemented, as in the starter.
    pass
