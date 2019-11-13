# from django.test import TestCase
import pytest
from unittest import mock

# import requests_mock

from model_bakery import baker

# from unittest.mock import MagicMock

from ranger.models import Ranger, WalletFunding
from payment.models import Payment
from payment.paystack import get_headers, initiate
from payment.views import new_payment, verify_paystack_payment


def test_mock_secret_key(settings):
    settings.PAYSTACK_SECRET_KEY = ""
    assert settings.PAYSTACK_SECRET_KEY == ""


@mock.patch("payment.paystack.settings", PAYSTACK_SECRET_KEY="test")
def test_get_headers(settings):
    # mocker.patch("payment.paystack.settings.SECRET_KEY", return_value="test")
    headers = get_headers()
    assert headers["Authorization"] == "Bearer test"


@mock.patch("payment.paystack.requests")
def test_initiate_returns_json(requests):
    requests.post.return_value.json.return_value = {
        "status": True,
        "message": "Authorization URL created",
        "data": {
            "authorization_url": "https://checkout.paystack.com/aaaaaaa",
            "access_code": "aaaaaaa",
            "reference": "xxx238923",
        },
    }
    resp = initiate("test@one.com", 1000, "xxx238923")
    assert resp["data"]["reference"] == "xxx238923"


@mock.patch("payment.paystack.requests")
def _test_initiate_bad_request(requests):
    requests.post.return_value.json.return_value = {
        "status": False,
        "message": "Invalid Email Address Passed",
    }


def create_ranger(user, balance=0):
    return Ranger.objects.create(
        user=user, first_name="a", last_name="b", phone="080", balance=balance
    )


@pytest.mark.django_db
def test_new_payment(rf, django_user_model):
    usr = django_user_model.objects.create_user(
        username="test@agent.com", password="passpass12345"
    )
    ranger = baker.make("ranger.Ranger", user=usr)
    # ranger = create_ranger(usr)
    # mock_ranger.get.return_value.user = usr

    with mock.patch("payment.paystack.requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "status": True,
            "message": "Authorization URL created",
            "data": {
                "authorization_url": "https://checkout.paystack.com/aaaaaaa",
                "access_code": "aaaaaaa",
                "reference": "xxx238923",
            },
        }
        params = {"email": "test@agent.com", "amount": 10000}
        request = rf.post("/payment/initiate/", params)
        response = new_payment(request)
        assert response.status_code == 200
        funding = WalletFunding.objects.filter(ranger=ranger)[0]
        assert funding.status == Payment.PENDING
        assert funding.amount == 100
        payment = funding.payment
        assert payment.status == Payment.PENDING
        assert payment.amount == 100


@pytest.mark.django_db
def test_verify(rf, django_user_model):
    usr = django_user_model.objects.create_user(
        username="test@agent.com", password="passpass12345"
    )
    ref = "xxxyyyzzz"
    ranger = baker.make("ranger.Ranger", user=usr, balance=100)
    payment = baker.make("payment.Payment", amount=100, status=0, reference=ref)
    funding = baker.make(
        "ranger.WalletFunding", ranger=ranger, payment=payment, amount=100, status=0
    )
    # mock the request
    with mock.patch("payment.paystack.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "status": True,
            "message": "Verification successful",
            "data": {"id": 1111},
        }
        url = "/payment/verify/?reference={}".format(ref)
        req = rf.get(url)
        response = verify_paystack_payment(req)
        assert response.status_code == 200
