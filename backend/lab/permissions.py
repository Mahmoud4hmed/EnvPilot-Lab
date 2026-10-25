from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from .models import Membership, Organization


def organization_for(user, org_id, write=False):
    org = get_object_or_404(Organization, pk=org_id)
    membership = Membership.objects.filter(user=user, organization=org).first()
    if not membership or (write and membership.role == 'viewer'):
        raise PermissionDenied('Organization membership/role does not allow this action.')
    return org
