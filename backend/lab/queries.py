from .models import Environment


def environment_rows(org_id):
    return Environment.objects.filter(project__organization_id=org_id).order_by('-id')
