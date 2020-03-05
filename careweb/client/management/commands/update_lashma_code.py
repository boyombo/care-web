from django.core.management.base import BaseCommand

from client.models import Client
from client.utils import get_quality_life_number


class Command(BaseCommand):

    def handle(self, *args, **options):
        code = 0
        salutation = 0
        for client in Client.objects.all():
            if not client.lashma_quality_life_no:
                client.lashma_quality_life_no = get_quality_life_number(client)
                code += 1
            if not client.salutation:
                client.salutation = client.get_salutation
                salutation += 1
            client.save()
        print("%s codes and %s salutations updated." % (code, salutation))
