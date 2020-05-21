from django.core.management.base import BaseCommand

from client.models import UploadedClient, Client


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Update initialized")
        updated = 0
        for item in UploadedClient.objects.all():
            phone = item.phone_number
            phone_number = phone.replace("234", "0", 1)
            if Client.objects.filter(phone_no=phone_number).exists():
                client = Client.objects.get(phone_no=phone_number)
                client.lashma_no = item.policy_number
                client.membership_number = item.membership_number
                client.save()
                updated += 1
            else:
                print(phone_number, item.full_name, item.policy_number)
        print("Upload: ", UploadedClient.objects.count(), " .Updated: ", updated)
        print("Done updating.")
