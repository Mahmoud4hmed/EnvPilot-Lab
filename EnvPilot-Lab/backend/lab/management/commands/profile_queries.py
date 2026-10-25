import json
from django.core.management.base import BaseCommand
from django.db import connection
from django.test.utils import CaptureQueriesContext
from lab.queries import environment_rows
from lab.serializers import EnvironmentSerializer


class Command(BaseCommand):
    help = 'Measure query growth and inspect PostgreSQL plan; no wall-clock grading.'
    def add_arguments(self, parser):
        parser.add_argument('--organization', type=int, default=1)
    def handle(self, *args, **opts):
        for size in [5, 20, 60]:
            with CaptureQueriesContext(connection) as queries:
                data = EnvironmentSerializer(environment_rows(opts['organization'])[:size], many=True).data
            self.stdout.write(json.dumps({'rows': len(data), 'queries': len(queries)}))
        rows = environment_rows(opts['organization']).filter(status='pending')[:60]
        self.stdout.write(rows.explain(analyze=True, buffers=True) if connection.vendor == 'postgresql' else rows.explain())
