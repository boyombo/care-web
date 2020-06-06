import json

from django.conf import settings

import requests

import base64

from client.models import Client
from core.models import Plan


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
    payload = "{\"messages\":[{\"from\":\"InfoSMS\",\"destinations\":[{\"to\":\"2347061543553\",\"messageId\":\"MESSAGE-ID-123-xyz\"}],\"text\":\"Testing sms.\",\"flash\":false,\"intermediateReport\":true}}"
    # payload = json.dumps(data)
    response = requests.post(url, headers=headers, data=payload)
    print(response.json())
    return response


def send_multi_sms(receivers, msg):
    key = settings.INFOBIP_KEY
    headers = {
        "Authorization": f"App {key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    url = "https://dmm56g.api.infobip.com/sms/2/text/single"
    data = {
        "from": "FutureCare",
        "to": receivers,
        "text": msg,
    }
    payload = json.dumps(data)
    response = requests.post(url, headers=headers, data=payload)
    return response.status_code


def get_client_contacts(category, plan_id, receivers):
    clients = []
    contacts = []
    if category == "P":
        plan = Plan.objects.get(id=plan_id)
        clients = plan.client_set.all()
    elif category == "A":
        clients = Client.objects.all()
    elif category == "C":
        clients = None