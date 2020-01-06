from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages

from ranger.models import WalletFunding, Ranger
from client.models import Client
from subscription.models import SubscriptionPayment
from subscription.utils import (
    create_subscription,
    get_subscription_rate,
)
from payment.models import Payment
from payment.forms import PaymentForm, WalkinPaymentForm
from payment.utils import get_reference, get_user_for_payment
from payment.paystack import initiate, verify
from core.basic import basic_auth, basic_error_response

import logging

logger = logging.getLogger(__name__)


def verify_user(request):
    _usr = basic_auth(request)
    if not _usr:
        return basic_error_response()

    username = request.GET.get("username", None)
    if not username:
        return HttpResponseBadRequest("Illegal request")

    try:
        user_details = get_user_for_payment(username)
    except ValueError as err:
        return HttpResponseBadRequest(err)
        # return JsonResponse({"success": False, "error": err})
    else:
        user_details.update({"success": True})
        return JsonResponse(user_details)

    # try:
    #    usr = User.objects.get(username=username)
    # except User.DoesNotExist:
    #    return JsonResponse({"success": False, "error": "This user does not exist"})

    # try:
    #    Client.objects.get(user=usr)
    # except Client.DoesNotExist:
    #    try:
    #        Ranger.objects.get(user=usr)
    #    except Ranger.DoesNotExist:
    #        return JsonResponse({"success": False, "error": "This user is not active"})
    #    else:
    #        return JsonResponse({"success": True})
    # else:
    #    return JsonResponse({"success": True})

    return HttpResponseBadRequest("Illegal request")


@csrf_exempt
def walkin_payment(request):
    _usr = basic_auth(request)
    if not _usr:
        return basic_error_response()

    if request.method == "POST":
        form = WalkinPaymentForm(request.POST)
        if form.is_valid():
            ref = get_reference()
            # import pdb;pdb.set_trace()
            usr = form.cleaned_data["user"]
            amount = form.cleaned_data["amount"]
            # reference from POST is actually saved as cust_reference
            # and an auto-generated ref is saved as reference
            cust_reference = form.cleaned_data["reference"]

            pymt = form.save(commit=False)
            pymt.cust_reference = cust_reference
            pymt.reference = ref
            pymt.status = Payment.SUCCESSFUL
            pymt.payment_mode = Payment.BANK_PAYMENT
            pymt.save()

            try:
                _client = Client.objects.get(user__username=usr)
            except Client.DoesNotExist:
                pass
            else:
                create_subscription(_client, amount)
                return JsonResponse({"success": True, "reference": ref})

            try:
                _ranger = Ranger.objects.get(user__username=usr)
            except Ranger.DoesNotExist:
                return JsonResponse({"success": False, "error": "User does not exist"})
            else:
                WalletFunding.objects.create(
                    ranger=_ranger,
                    amount=amount,
                    bank="Fidelity",
                    name=pymt.paid_by,
                    reference=ref,
                    payment_type=WalletFunding.BANK_DEPOSIT,
                    payment=pymt,
                    status=WalletFunding.SUCCESSFUL,
                )
                _ranger.balance += pymt.amount
                _ranger.save()
                return JsonResponse({"success": True, "reference": ref})
        else:
            errors = form.errors.as_json()
            return JsonResponse({"success": False, "errors": errors})
    else:
        return JsonResponse({"success": False, "errors": "Only POST allowed"})


## Paystack


def paystack_initiate_subscription(request):
    email = request.user.username
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        return redirect("paystack_error")
    else:
        amount = get_subscription_rate(client)
        # kobo = amount * 100
        reference = get_reference()
        pymt = Payment.objects.create(amount=amount, reference=reference)
        logger.info("payment created")

        SubscriptionPayment.objects.create(
            client=client,
            amount=amount,
            payment=pymt,
            payment_type=SubscriptionPayment.CARD,
        )
        res = initiate(email, amount, reference)
        logger.info(res)
        if res["status"]:
            auth_url = res["data"]["authorization_url"]
            return redirect(auth_url)
        else:
            return JsonResponse(res)


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
            logger.info("Payment created")
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
                    logger.info("creating subscription for client")
                    SubscriptionPayment.objects.create(
                        client=client,
                        amount=amount / 100.0,
                        payment=pymt,
                        payment_type=SubscriptionPayment.CARD,
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
            return redirect("paystack_error")
        else:
            resp = verify(pymt)
            logger.info("success")
            logger.info(resp)
            pymt.status = Payment.SUCCESSFUL
            pymt.save()
            try:
                sub_payment = SubscriptionPayment.objects.get(payment=pymt)
            except SubscriptionPayment.DoesNotExist:
                try:
                    funding = WalletFunding.objects.get(payment=pymt)
                except WalletFunding.DoesNotExist:
                    logger.info(
                        "Problem finding source for transaction {}".format(txref)
                    )
                    return redirect("paystack_error")
                else:
                    funding.status = WalletFunding.SUCCESSFUL
                    funding.save()
                    ranger = funding.ranger
                    ranger.balance += pymt.amount
                    ranger.save()
                    messages.success(request, "Payment successful")
                    return redirect("/admin/ranger/walletfunding/")
            else:
                sub_payment.status = SubscriptionPayment.SUCCESSFUL
                sub_payment.save()
                create_subscription(sub_payment.client, sub_payment.amount)
                if request.user.is_authenticated:
                    return redirect("profile")
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
    ref = request.GET.get("reference")
    pymt = get_object_or_404(Payment, reference=ref)
    subscription_payment = SubscriptionPayment.objects.get(payment=pymt)
    client = subscription_payment.client
    logger.info(client)

    # funding = WalletFunding.objects.get(payment=pymt)
    # ranger = funding.ranger
    resp = verify(pymt)
    logger.info(resp)
    if (
        pymt.status == Payment.PENDING
        and subscription_payment.status == SubscriptionPayment.PENDING
    ):
        pymt.status = Payment.SUCCESSFUL
        pymt.save()
        subscription_payment.status = SubscriptionPayment.SUCCESSFUL
        subscription_payment.save()

        _sub = create_subscription(client, subscription_payment.amount)
        expiry = _sub.expiry_date.strftime("%d %b %Y")

        # funding.status = WalletFunding.SUCCESSFUL
        # funding.save()

        # ranger.balance += pymt.amount
        # ranger.save()
    return JsonResponse({"success": True, "expiry": expiry})
