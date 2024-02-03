from django.core.management.base import BaseCommand

from myproject.myapp2.models import Client


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        clients = Client.object.all()
        self.stdout.write(f'{clients}')
