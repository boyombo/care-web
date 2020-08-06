import base64

import requests
from django.core.management.base import BaseCommand
import json

from careweb import settings
from client.models import Client
from sms.utils import send_multi_sms, format_number


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--sender')

    def handle(self, *args, **options):
        sender = options.get("sender")
        sender = sender if sender else "FutureCare"
        success = 0
        failure = 0
        skipped = 0
        for client in Client.objects.filter(verified=True):
            if client.lashma_no and client.phone_no:
                msg = "Dear {name}, your Quality Life Code is {ql_code} and LASHMA ID is {lashma_id}. " \
                      "Kindly Keep them safe for subsequent Use. Thank you.".format(name=client.full_name,
                                                                                    ql_code=client.lashma_quality_life_no,
                                                                                    lashma_id=client.lashma_no)
                phone = format_number(client.phone_no)
                phone_number = phone.replace("0", "234", 1) if str(phone).startswith("0") else phone
                if len(phone_number) < 13:
                    continue
                status = send_multi_sms([phone_number], msg, sender)
                if str(status) == "200":
                    success += 1
                else:
                    failure += 1
            else:
                skipped += 1
        print("{} succeeded, {} failed and {} was skipped".format(success, failure, skipped))
