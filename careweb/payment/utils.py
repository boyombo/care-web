from random import sample
from django.contrib.auth.models import User


from client.models import Client
from payment.models import Payment
from ranger.models import WalletFunding, Ranger
from subscription.utils import get_subscription_rate

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


def get_user_for_payment(username):
    try:
        usr = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError("This user does not exist")
        # return JsonResponse({"success": False, "error": "This user does not exist"})

    try:
        _client = Client.objects.get(user=usr)
    except Client.DoesNotExist:
        try:
            _ranger = Ranger.objects.get(user=usr)
        except Ranger.DoesNotExist:
            raise ValueError("This user is not active")
            # return JsonResponse({"success": False, "error": "This user is not active"})
        else:
            return {
                "first_name": _ranger.first_name,
                "last_name": _ranger.last_name,
            }
            # return "ranger"
            # return JsonResponse({"success": True})
    else:
        return {"first_name": _client.first_name, "last_name": _client.surname}
        # return "client"
        # return JsonResponse({"success": True})


def get_details_for_ussd(phone):
    try:
        _client = Client.objects.get(phone_no=phone)
    except Client.DoesNotExist:
        raise ValueError("User does not exist")
    else:
        return {"amount": get_subscription_rate(_client)}
