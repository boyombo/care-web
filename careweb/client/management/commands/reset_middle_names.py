from datetime import datetime

from django.core.management.base import BaseCommand

from client.models import Client, Dependant


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--date')

    def handle(self, *args, **options):
        updated_clients = 0
        updated_dependants = 0
        for client in Client.objects.all():
            if not client.middle_name or client.middle_name == "None":
                client.middle_name = ""
                client.save()
                updated_clients += 1
        for dependant in Dependant.objects.all():
            if not dependant.middle_name or dependant.middle_name == "None":
                dependant.middle_name = ""
                dependant.save()
                updated_dependants += 1

        print("%s clients, %s dependants updated" % (updated_clients, updated_dependants))
