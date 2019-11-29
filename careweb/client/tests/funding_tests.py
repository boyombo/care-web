import pytest
from model_bakery import baker

from payment.models import Payment
from ranger.models import Ranger, WalletFunding
from payment.utils import approve_funding


@pytest.fixture
def ranger():
    ranger = baker.make("ranger.Ranger", balance=100)
    return ranger


@pytest.fixture
def payment():
    return baker.make("payment.Payment", amount=100)


@pytest.mark.django_db
def test_funding_balance(ranger, payment):
    funding = baker.make(
        "ranger.WalletFunding", ranger=ranger, payment=payment, amount=100
    )
    approve_funding(funding)
    assert ranger.balance == 200


@pytest.mark.django_db
def test_funding_status(ranger, payment):
    funding = baker.make(
        "ranger.WalletFunding", ranger=ranger, payment=payment, amount=100
    )
    approve_funding(funding)
    assert funding.status == WalletFunding.SUCCESSFUL
    assert payment.status == Payment.SUCCESSFUL


@pytest.mark.django_db
def test_approve_funding_success_status(ranger, payment):
    funding = baker.make(
        "ranger.WalletFunding",
        ranger=ranger,
        payment=payment,
        amount=100,
        status=WalletFunding.SUCCESSFUL,
    )
    approve_funding(funding)
    assert ranger.balance == 100


@pytest.mark.django_db
def test_approve_funding_failed_status(ranger, payment):
    funding = baker.make(
        "ranger.WalletFunding",
        ranger=ranger,
        payment=payment,
        amount=100,
        status=WalletFunding.FAILED,
    )
    approve_funding(funding)
    assert ranger.balance == 100
