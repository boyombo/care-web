import json

from django.conf import settings

import requests


def send_sms(msisdn, msg):
    key = settings.INFOBIP_KEY
    headers = {
        "Authorization": f"App {key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    url = "https://api.infobip.com/sms/2/text/advanced"
    data = {
        "message": [
            {
                "from": "FutureCare",
                "destinations": [{"to": f"234{msisdn[-10:]}"}],
                "text": msg,
                "flash": False,
            }
        ]
    }
    payload = json.dumps(data)
    response = requests.post(url, headers=headers, data=payload)
    return response
