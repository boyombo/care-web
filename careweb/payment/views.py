from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from ranger.models import WalletFunding, Ranger
from client.models import Client, Subscription
from payment.models import Payment
from payment.forms import PaymentForm
from payment.utils import get_reference
from payment.paystack import initiate, verify

import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def new_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            amount = form.cleaned_data["amount"]
            kobo = amount

            reference = get_reference()
            pymt = Payment.objects.create(amount=kobo / 100.0, reference=reference)
            usr = User.objects.get(username=email)

            # a ranger or a client?
            try:
                ranger = Ranger.objects.get(user=usr)
            except Ranger.DoesNotExist:
                try:
                    client = Client.objects.get(user=usr)
                except Client.DoesNotExist:
                    return JsonResponse(
                        {"success": False, "error": "Account does not exist"}
                    )
                else:
                    Subscription.objects.create(
                        client=client, amount=amount / 100.0, payment=pymt
                    )
            else:
                WalletFunding.objects.create(
                    ranger=ranger,
                    amount=kobo / 100.0,
                    payment=pymt,
                    status=WalletFunding.PENDING,
                    bank="Paystack",
                )
            res = initiate(email, kobo, reference)
            logger.info(res)
            # data = res.json()
            # logger.info(data)
            print(res)
            if res["status"]:
                access_code = res["data"]["access_code"]
                return JsonResponse({"success": True, "access_code": access_code})
        else:
            logger.error(form.errors)
    return JsonResponse({"success": False})


@csrf_exempt
def paystack_callback(request):
    if request.method == "POST":
        logger.info("Payment Response")
        logger.info(request.POST)
        # data = json.loads(request.POST["resp"])
        return JsonResponse({"success": True})
    else:
        logger.info("GET response")
        logger.info(request.GET)
        txref = request.GET.get("trxref")
        try:
            pymt = Payment.objects.get(reference=txref)
        except Payment.DoesNotExist:
            # redirect to error page
            logger.info("error")
            pymt.status = Payment.FAILED
            pymt.save()
            funding = WalletFunding.objects.get(payment=pymt)
            funding.status = WalletFunding.FAILED
            return redirect("paystack_error")
        else:
            resp = verify(pymt)
            logger.info("success")
            logger.info(resp)
            pymt.status = Payment.SUCCESSFUL
            pymt.save()
            funding = WalletFunding.objects.get(payment=pymt)
            funding.status = WalletFunding.SUCCESSFUL
            funding.save()
            ranger = funding.ranger
            ranger.balance += pymt.amount
            ranger.save()
            return redirect("paystack_success")


def paystack_success(request):
    return JsonResponse({"success": True})


def paystack_error(request):
    return JsonResponse({"success": False})


def verify_paystack_payment(request):
    # TODO: process failed verifications as well
    ref = request.GET.get("reference")
    pymt = get_object_or_404(Payment, reference=ref)
    funding = WalletFunding.objects.get(payment=pymt)
    ranger = funding.ranger
    resp = verify(pymt)
    logger.info(resp)
    if pymt.status == Payment.PENDING:
        pymt.status = Payment.SUCCESSFUL
        pymt.save()

        funding.status = WalletFunding.SUCCESSFUL
        funding.save()

        ranger.balance += pymt.amount
        ranger.save()
    return JsonResponse({"success": True, "balance": "{}".format(ranger.balance)})


def verify_paystack_subscription(request):
    # TODO: start and end dates for subscription, status of subscription
    ref = request.GET.get("reference")
    pymt = get_object_or_404(Payment, reference=ref)
    subscription = Subscription.objects.get(payment=pymt)
    client = subscription.client
    logger.info(client)

    # funding = WalletFunding.objects.get(payment=pymt)
    # ranger = funding.ranger
    resp = verify(pymt)
    logger.info(resp)
    if pymt.status == Payment.PENDING:
        pymt.status = Payment.SUCCESSFUL
        pymt.save()

        # funding.status = WalletFunding.SUCCESSFUL
        # funding.save()

        # ranger.balance += pymt.amount
        # ranger.save()
    return JsonResponse({"success": True})
