from django.core.management.base import BaseCommand
from django.db.models import Q

from client.models import UploadedClient


class Command(BaseCommand):

    def handle(self, *args, **options):
        for item in UploadedClient.objects.all():
            phone = item.phone_number
            phone_number = phone.replace("234", "0", 1)

