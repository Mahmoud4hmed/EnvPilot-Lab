from django.conf import settings
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=80, unique=True)


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=[('owner', 'Owner'), ('developer', 'Developer'), ('viewer', 'Viewer')])
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'organization'], name='unique_membership')]


class Project(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)


class Environment(models.Model):
    STATES = [(s, s) for s in ['pending', 'provisioning', 'ready', 'failed']]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    status = models.CharField(max_length=16, choices=STATES, default='pending')
    provider_id = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Operation(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    kind = models.CharField(max_length=20, default='provision')
    key = models.CharField(max_length=80)
    fingerprint = models.CharField(max_length=64)
    scenario = models.CharField(max_length=32, default='success')
    status = models.CharField(max_length=16, default='queued')
    attempts = models.PositiveIntegerField(default=0)
    error = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    environment = models.ForeignKey(Environment, related_name='events', on_delete=models.CASCADE)
    message = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)


class SupportDocument(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
