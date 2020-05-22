import json

from django.conf import settings

import requests

import base64


def send_sms(msisdn="7061543553", msg="Test"):
    key = settings.INFOBIP_KEY
    print("Key", key)

    encoded = base64.b64encode(b"Futureview01:@fuTureCare20").decode("utf-8")
    print(encoded)

    headers = {
        # "Authorization": f"App {key}",
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    # url = "https://dmm56g.api.infobip.com/sms/2/text/advanced"
    url = "https://api.infobip.com/sms/2/text/advanced"
    data = {
        "message": [
            {
                "from": "InfoSMS",
                # "from": "FutureCare",
                "destinations": [{"to": f"234{msisdn[-10:]}"}],
                "text": msg,
                "flash": False,
            }
        ]
    }
    payload = json.dumps(data)
    response = requests.post(url, headers=headers, data=payload)
    print(response.json())
    return response
