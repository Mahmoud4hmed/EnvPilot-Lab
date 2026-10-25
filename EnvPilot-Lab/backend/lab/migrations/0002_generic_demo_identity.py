from django.conf import settings
from django.db import migrations


def rename_demo_data(apps, schema_editor):
    User=apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    Organization=apps.get_model('lab','Organization')
    Membership=apps.get_model('lab','Membership')
    Project=apps.get_model('lab','Project')
    Document=apps.get_model('lab','SupportDocument')
    alias=schema_editor.connection.alias
    for old_name,new_name,username in [('Nile Labs','Team Alpha','owner'),('Delta Works','Team Beta','other_owner')]:
        org=Organization.objects.using(alias).filter(name=old_name).first()
        if org is None:
            continue
        if Organization.objects.using(alias).filter(name=new_name).exclude(pk=org.pk).exists():
            raise RuntimeError(f'Both legacy and generic demo organizations exist: {new_name}. Resolve the duplicate before migrating; no data has been reset.')
        membership=Membership.objects.using(alias).filter(organization_id=org.pk,role='owner').order_by('pk').first()
        if membership:
            user=User.objects.using(alias).get(pk=membership.user_id)
            if user.username!=username:
                if User.objects.using(alias).filter(username=username).exclude(pk=user.pk).exists():
                    raise RuntimeError(f'Demo username {username} already belongs to another account; migration refuses to merge users.')
                user.username=username
                user.first_name='';user.last_name=''
                user.save(using=alias,update_fields=['username','first_name','last_name'])
        org.name=new_name
        org.save(using=alias,update_fields=['name'])
        for project in Project.objects.using(alias).filter(organization_id=org.pk,name__startswith=old_name+' project '):
            project.name=project.name.replace(old_name,new_name,1)
            project.save(using=alias,update_fields=['name'])
        for document in Document.objects.using(alias).filter(organization_id=org.pk,content__contains=old_name):
            document.content=document.content.replace(old_name,new_name)
            document.save(using=alias,update_fields=['content'])


class Migration(migrations.Migration):
    dependencies=[('lab','0001_initial'),migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[migrations.RunPython(rename_demo_data,migrations.RunPython.noop)]
