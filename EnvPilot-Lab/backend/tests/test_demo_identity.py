import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management import call_command
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from rest_framework.authtoken.models import Token


@pytest.mark.django_db(transaction=True)
def test_generic_identity_migration_preserves_learner_data_and_passwords():
    executor=MigrationExecutor(connection)
    before=[('lab','0001_initial')]
    after=[('lab','0002_generic_demo_identity')]
    executor.migrate(before)
    apps=executor.loader.project_state(before).apps
    User=apps.get_model('auth','User')
    Org=apps.get_model('lab','Organization')
    Membership=apps.get_model('lab','Membership')
    Project=apps.get_model('lab','Project')
    Environment=apps.get_model('lab','Environment')
    Operation=apps.get_model('lab','Operation')
    Event=apps.get_model('lab','Event')
    Document=apps.get_model('lab','SupportDocument')
    owner=User.objects.create(username='legacy_primary',password=make_password('KeepMe123!'),first_name='Demo',last_name='Person')
    other=User.objects.create(username='legacy_secondary',password=make_password('KeepMe123!'))
    org=Org.objects.create(name='Nile Labs')
    second=Org.objects.create(name='Delta Works')
    membership=Membership.objects.create(user_id=owner.pk,organization=org,role='owner')
    Membership.objects.create(user_id=other.pk,organization=second,role='owner')
    project=Project.objects.create(organization=org,name='Nile Labs project 1')
    env=Environment.objects.create(project=project,name='dev-1-001',status='ready',provider_id='vm-keep')
    operation=Operation.objects.create(organization=org,environment=env,key='keep-operation',fingerprint='keep-fingerprint',status='succeeded',attempts=2)
    event=Event.objects.create(environment=env,message='Keep learner investigation evidence')
    doc=Document.objects.create(organization=org,title='Provisioning',content='Nile Labs: existing support notes')
    token=Token.objects.create(user_id=owner.pk,key='a'*40)
    try:
        executor=MigrationExecutor(connection)
        executor.migrate(after)
        renamed=get_user_model().objects.get(pk=owner.pk)
        assert renamed.username=='owner' and renamed.check_password('KeepMe123!')
        assert renamed.first_name==renamed.last_name==''
        assert Token.objects.get(user_id=owner.pk).key==token.key
        from lab.models import Organization,Project as CurrentProject,Environment as CurrentEnvironment,Operation as CurrentOperation,Event as CurrentEvent,Membership as CurrentMembership,SupportDocument
        assert Organization.objects.get(pk=org.pk).name=='Team Alpha'
        assert Organization.objects.get(pk=second.pk).name=='Team Beta'
        assert get_user_model().objects.get(pk=other.pk).username=='other_owner'
        assert CurrentMembership.objects.get(pk=membership.pk).user_id==owner.pk
        assert CurrentProject.objects.get(pk=project.pk).name=='Team Alpha project 1'
        assert CurrentEnvironment.objects.get(pk=env.pk).provider_id=='vm-keep'
        assert CurrentOperation.objects.get(pk=operation.pk).attempts==2
        assert CurrentEvent.objects.get(pk=event.pk).message=='Keep learner investigation evidence'
        assert SupportDocument.objects.get(pk=doc.pk).content=='Team Alpha: existing support notes'
        call_command('seed');count=CurrentEnvironment.objects.count();call_command('seed')
        assert CurrentEnvironment.objects.count()==count==480
        assert Organization.objects.count()==2
        assert CurrentEnvironment.objects.get(pk=env.pk).status=='ready'
        assert get_user_model().objects.get(username='owner').check_password('KeepMe123!')
    finally:
        MigrationExecutor(connection).migrate(after)
