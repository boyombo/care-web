from datetime import datetime

from django.core.management.base import BaseCommand

from client.models import Client


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--date')

    def handle(self, *args, **options):
        updated = 0
        for client in Client.objects.all():
            if not client.lashma_no or client.lashma_no == "None":
                client.lashma_no = ""
                client.save()
                updated += 1
        print("%s clients updated" % updated)
