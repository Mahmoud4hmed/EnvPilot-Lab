from django.conf import settings
from django.db import migrations


def rename_demo_data(apps,schema_editor):
    User=apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    Team=apps.get_model('mockapp','Team')
    Member=apps.get_model('mockapp','Member')
    alias=schema_editor.connection.alias
    for old_name,new_name,username in [('Nile','Team Alpha','owner'),('Delta','Team Beta','other_owner')]:
        team=Team.objects.using(alias).filter(name=old_name).first()
        if team is None:continue
        if Team.objects.using(alias).filter(name=new_name).exclude(pk=team.pk).exists():
            raise RuntimeError('Duplicate demo teams; migration refuses to merge data.')
        member=Member.objects.using(alias).filter(team_id=team.pk,role='owner').first()
        if member:
            user=User.objects.using(alias).get(pk=member.user_id)
            if user.username!=username:
                if User.objects.using(alias).filter(username=username).exclude(pk=user.pk).exists():
                    raise RuntimeError('Demo username collision; migration refuses to merge accounts.')
                user.username=username;user.first_name='';user.last_name=''
                user.save(using=alias,update_fields=['username','first_name','last_name'])
        team.name=new_name;team.save(using=alias,update_fields=['name'])


class Migration(migrations.Migration):
    dependencies=[('mockapp','0001_initial'),migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[migrations.RunPython(rename_demo_data,migrations.RunPython.noop)]
