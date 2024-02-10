from django.core.management.base import BaseCommand

from .myapp2.models import Client


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        client = Client(name='John Doe', email='john@example.com', phone='1234567890', address='123 Main St')
        client.save()
        self.stdout.write(f'{client}')