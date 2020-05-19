from django.core.management.base import BaseCommand
from django.db.models import Q

from client.models import UploadedClient, Client


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Clients in spreadsheet but not in DB")
        not_in_db = 0
        for item in UploadedClient.objects.all():
            phone = item.phone_number
            phone_number = phone.replace("234", "0", 1)
            if not Client.objects.filter(phone_no=phone_number).exists():
                print(phone_number, item.full_name, item.policy_number)
                not_in_db += 1
        print(not_in_db, "clients not found in the DB")

        print("=========================================================")
        print("Clients in DB but not on spreadsheet")
        not_in_sheet = 0
        for client in Client.objects.all():
            phone = client.phone_no
            phone_number = phone.replace("0", "234", 1) if phone and str(phone).startswith("0") else phone
            if not UploadedClient.objects.filter(phone_number=phone_number).exists():
                print(phone_number, client.full_name, client.lashma_no)
                not_in_sheet += 1
        print(not_in_sheet, "clients not found in spreadsheet")
