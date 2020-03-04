from django.core.management.base import BaseCommand

from client.models import Dependant


class Command(BaseCommand):

    def handle(self, *args, **options):
        count = 0
        for dependant in Dependant.objects.all():
            if not dependant.salutation:
                dependant.salutation = dependant.get_salutation
                dependant.save()
                count += 1

        print("%s dependants updated" % count)
