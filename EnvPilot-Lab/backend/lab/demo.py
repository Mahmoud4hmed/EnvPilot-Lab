"""Explicitly enabled local teaching convenience; product endpoints still authenticate normally."""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Membership

DEMO_USERS=('owner','developer','viewer','other_owner','dual','outsider')


class DemoSession(APIView):
    permission_classes=[AllowAny]
    authentication_classes=[]

    def post(self,request):
        if not settings.LAB_DEMO_ROLE_SWITCH:
            raise Http404()
        role=request.data.get('role')
        if not isinstance(role,str) or role not in DEMO_USERS:
            raise ValidationError({'role':'Choose an existing demo role.'})
        user=get_user_model().objects.filter(username=role,is_active=True,is_staff=False,is_superuser=False).first()
        if user is None:
            raise ValidationError({'role':'Demo account unavailable. Run python lab.py seed.'})
        token,_=Token.objects.get_or_create(user=user)
        memberships=Membership.objects.filter(user=user).select_related('organization').order_by('organization_id')
        response=Response({'username':user.username,'token':token.key,'memberships':[{'organization':m.organization_id,'name':m.organization.name,'role':m.role} for m in memberships]})
        response['Cache-Control']='no-store'
        return response
