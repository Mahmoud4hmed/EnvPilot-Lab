from django.db import models
from django.conf import settings


class Team(models.Model):
    name = models.CharField(max_length=80, unique=True)


class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=12)


class Memo(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    archived_at = models.DateTimeField(null=True)


class Audit(models.Model):
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE)
    action = models.CharField(max_length=40)
