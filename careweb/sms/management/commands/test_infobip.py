import base64

import requests
from django.core.management.base import BaseCommand
import json

from careweb import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        key = settings.INFOBIP_KEY
        msg = "Testing Infobip"
        msisdn = "2347061543553"

        # encoded = base64.b64encode(b"Futureview01:@fuTureCare20").decode("utf-8")
        # print(encoded)

        headers = {
            "Authorization": f"App {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        url = "https://dmm56g.api.infobip.com/sms/2/text/single"
        # data = {
        #     "messages": [
        #         {
        #             "from": "InfoSMS",
        #             "destinations": [{"to": f"234{msisdn[-10:]}"}],
        #             "text": msg,
        #             "flash": False,
        #         }
        #     ]
        # }
        data = {
            "from": "FutureCare",
            "to": [f"234{msisdn[-10:]}", "2348142828158"],
            "text": msg,
        }
        payload = json.dumps(data)
        print(payload)
        response = requests.post(url, headers=headers, data=payload)
        print(response.status_code)
