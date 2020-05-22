from django.core.management.base import BaseCommand

from client.models import Client


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Initialized")
        phones = []
        for client in Client.objects.all():
            phone = client.phone_no
            if not phone:
                continue
            phone_number = phone.replace("0", "234", 1) if str(phone).startswith("0") else phone
            phones.append(phone_number)

        print(",".join(phones))
