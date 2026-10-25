from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from mockapp.models import Team,Member,Memo


class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        for name,team_name,role in [('owner','Team Alpha','owner'),('viewer','Team Alpha','viewer'),('other_owner','Team Beta','owner')]:
            team,_=Team.objects.get_or_create(name=team_name)
            user,new=get_user_model().objects.get_or_create(username=name)
            if new:
                user.set_password('LabPass123!');user.save()
            Member.objects.get_or_create(user=user,defaults={'team':team,'role':role})
            Memo.objects.get_or_create(team=team,title='Environment handover')
        self.stdout.write('Independent mock data ready')
