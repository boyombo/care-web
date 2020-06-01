from django.core.management.base import BaseCommand

from core.models import Plan


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--code')

    def handle(self, *args, **options):
        print("Initialized")
        print("Name,Phone")
        phones = []
        code = options.get("code")
        plan = Plan.objects.get(code__iexact=code)
        clients = plan.client_set.all()
        for client in clients:
            phone = client.phone_no
            if not phone:
                continue
            phone_number = phone.replace("0", "234", 1) if str(phone).startswith("0") else phone
            if len(phone_number) < 13:
                continue
            phones.append(phone_number)
            print("{},{}".format(client.full_name, phone_number))

        # print(",".join(phones))
