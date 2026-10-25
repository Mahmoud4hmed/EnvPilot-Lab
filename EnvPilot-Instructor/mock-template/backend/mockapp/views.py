from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Memo


def health(request):
    return JsonResponse({'status':'ok'})


def payload(memo):
    return {'id':memo.id,'title':memo.title,'archived_at':memo.archived_at}


def scoped(user, pk):
    return get_object_or_404(Memo, pk=pk, team=user.member.team)


class Memos(APIView):
    def get(self, request):
        return Response([payload(m) for m in Memo.objects.filter(team=request.user.member.team).order_by('id')])


class MemoDetail(APIView):
    def patch(self, request, pk):
        memo = scoped(request.user, pk)
        if request.user.member.role != 'owner':
            raise PermissionDenied()
        title = request.data.get('title')
        if not isinstance(title, str) or not title.strip() or len(title) > 60:
            raise ValidationError({'title':'Required nonblank string, max 60 chars.'})
        memo.title = title; memo.save(update_fields=['title'])
        return Response(payload(memo))


class Archive(APIView):
    # New product request is specified only in TASKS.md.
    pass
