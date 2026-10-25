from rest_framework import serializers
from .models import Environment, Operation


class EnvironmentSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    organization = serializers.IntegerField(source='project.organization_id', read_only=True)
    organization_name = serializers.CharField(source='project.organization.name', read_only=True)
    latest_event = serializers.SerializerMethodField()
    def get_latest_event(self, obj):
        event = obj.events.order_by('-id').first()
        return event.message if event else None
    class Meta:
        model = Environment
        fields = ['id', 'name', 'project', 'project_name', 'organization', 'organization_name', 'status', 'provider_id', 'latest_event', 'created_at', 'updated_at']
        read_only_fields = ['status', 'provider_id', 'created_at', 'updated_at']


class EnvironmentInput(serializers.Serializer):
    name = serializers.CharField(max_length=64, allow_blank=True)
    project = serializers.IntegerField(min_value=1)


class ProvisionInput(serializers.Serializer):
    scenario = serializers.ChoiceField(choices=['success', 'transient', 'lost_response', 'permanent'], default='success')


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['id', 'environment', 'kind', 'key', 'status', 'attempts', 'error', 'created_at']
