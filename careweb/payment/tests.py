# from django.test import TestCase
import pytest

from payment.paystack import get_headers


def test_mock_secret_key(settings):
    settings.PAYSTACK_SECRET_KEY = ""
    assert settings.PAYSTACK_SECRET_KEY == ""


def test_get_headers(mocker):
    mocker.patch("payment.paystack.settings")
    # settings.PAYSTACK_SECRET_KEY = ""
    headers = get_headers()
    assert headers["Authorization"] == "Bearer "
