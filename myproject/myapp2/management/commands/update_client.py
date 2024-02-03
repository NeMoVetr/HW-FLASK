from django.core.management.base import BaseCommand

from myproject.myapp2.models import Client


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('pk', type=int)
        parser.add_argument('name', type=str)

    def handle(self, *args, **kwargs):
        pk = kwargs.get('pk')
        name = kwargs.get('name')
        client = Client.object.filter(pk=pk).first()
        client.name = name
        client.save()
        self.stdout.write(f'{client}')