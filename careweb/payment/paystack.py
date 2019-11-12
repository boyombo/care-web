import requests

import logging

logger = logging.getLogger(__name__)

from django.conf import settings


SECRET_KEY = settings.PAYSTACK_SECRET_KEY
PUBLIC_KEY = settings.PAYSTACK_PUBLIC_KEY
INITIATE_URL = "https://api.paystack.co/transaction/initialize/"
VERIFY_URL = "https://api.paystack.co/transaction/verify/"

# REF = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"


# def get_reference():
#    return "".join(sample(REF, 30))


def get_headers():
    headers = {
        "Authorization": "Bearer {}".format(SECRET_KEY),
        "Content-Type": "application/json",
    }
    return headers


def initiate(email, amount, ref):
    headers = get_headers()
    logger.info(headers)
    # ref = get_reference()
    params = {"email": email, "amount": amount * 100, "reference": ref}
    resp = requests.post(INITIATE_URL, json=params, headers=headers)
    data = resp.json()
    logger.info(data)
    return data


def verify(payment):
    headers = get_headers()
    url = "{}{}".format(VERIFY_URL, payment.reference)
    resp = requests.get(url, headers=headers)
    data = resp.json()
    logger.info(data)
    return data
