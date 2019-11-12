from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from ranger.models import WalletFunding, Ranger
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
            kobo = amount * 100

            reference = get_reference()
            pymt = Payment.objects.create(amount=amount, reference=reference)
            usr = User.objects.get(username=email)
            ranger = Ranger.objects.get(user=usr)
            WalletFunding.objects.create(
                ranger=ranger,
                amount=amount,
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
            ranger.wallet_balance += pymt.amount
            ranger.save()
            return redirect("paystack_success")


def paystack_success(request):
    return JsonResponse({"success": True})


def paystack_error(request):
    return JsonResponse({"success": False})
