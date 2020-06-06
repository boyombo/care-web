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
    payload = json.dumps(data)
    response = requests.post(url, headers=headers, data=payload)
    print(response.json())
    return response


def send_multi_sms(receivers, msg, sender):
    key = settings.INFOBIP_KEY
    headers = {
        "Authorization": f"App {key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    url = "https://dmm56g.api.infobip.com/sms/2/text/single"
    data = {
        "from": sender,
        "to": receivers,
        "text": msg,
    }
    payload = json.dumps(data)
    response = requests.post(url, headers=headers, data=payload)
    return response.status_code


def get_client_contacts(category, plan, recipients):
    clients = []
    contacts = []
    if category == "P":
        clients = plan.client_set.all()
    elif category == "A":
        clients = Client.objects.all()
    elif category == "C":
        clients = None

    if clients:
        for client in clients:
            phone = client.phone_no
            if not phone:
                continue
            phone = format_number(phone)
            phone_number = phone.replace("0", "234", 1) if str(phone).startswith("0") else phone
            if len(phone_number) < 13:
                continue
            contacts.append(phone_number.strip())
    elif recipients:
        temp = recipients.split(",")
        for item in temp:
            item = format_number(item)
            phone_number = item.replace("0", "234", 1) if str(item).startswith("0") else item
            if len(phone_number) < 13:
                continue
            contacts.append(phone_number.strip())
    return contacts


def format_number(number):
    number = number[1:] if str(number).startswith("+") else number
    return number
