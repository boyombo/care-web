from datetime import datetime

from django.core.management.base import BaseCommand

from ranger.models import Ranger


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--date')

    def handle(self, *args, **options):
        updated = 0
        current = datetime.strptime("03/23/2020", "%m/%d/%Y")
        date = options.get("date")
        if date:
            default = datetime.strptime(date, "%m/%d/%Y")
        else:
            default = datetime.strptime("03/02/2020", "%m/%d/%Y")
        for ranger in Ranger.objects.all():
            if ranger.created.date() == current.date():
                ranger.created = default
                ranger.save()
                updated += 1
        print("%s rangers updated" % updated)
