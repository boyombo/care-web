from random import sample

from payment.models import Payment
from ranger.models import WalletFunding

REF = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"


def get_reference():
    return "".join(sample(REF, 30))


def approve_funding(funding):
    if funding.status != WalletFunding.PENDING:
        return False
    payment = funding.payment
    ranger = funding.ranger

    payment.status = Payment.SUCCESSFUL
    payment.save()

    funding.status = WalletFunding.SUCCESSFUL
    funding.save()

    ranger.balance += funding.amount
    ranger.save()
    return True
