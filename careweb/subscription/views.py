from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.base import TemplateView

from client.models import Client
from subscription.forms import SubscriptionForm
from subscription.models import SubscriptionPayment
from payment.models import Payment
from payment.utils import get_reference
from subscription import utils
from core.crypto import Encryptor, get_hash
from django.conf import settings


class SubscriptionView(TemplateView):
    def get_context_data(self, **kwargs):
        client = Client.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context["object"] = client
        self.client = client
        return context


class NewSubscriptionView(SubscriptionView):
    template_name = "subscription/new.html"


def card_subscription(request):
    client = get_object_or_404(Client, user=request.user)
    order_id = get_reference()
    amount = utils.get_subscription_rate(client)
    pymt = Payment.objects.create(
        amount=amount, reference=order_id, payment_mode=Payment.CARD_PAYMENT
    )
    SubscriptionPayment.objects.create(
        client=client,
        payment=pymt,
        payment_type=SubscriptionPayment.CARD,
        amount=amount,
    )

    encryptor = Encryptor()
    priv_key = encryptor.generate_string(16)
    encrypted = encryptor.encrypt(priv_key)
    _hash = get_hash(order_id, amount, priv_key)
    return render(
        request,
        "subscription/card.html",
        {
            "object": client,
            "hash": _hash,
            "encryptedKey": encrypted,
            "client": client,
            "orderId": order_id,
            "amt": amount,
            "currCode": "566",
            "mercId": settings.PAYGATE_MERCHANT_ID,
        },
    )


class CardSubscriptionView(SubscriptionView):
    template_name = "subscription/card.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # import pdb;pdb.set_trace()
        encryptor = Encryptor()
        priv_key = encryptor.generate_string(16)
        encrypted = encryptor.encrypt(priv_key)
        merchant_id = settings.PAYGATE_MERCHANT_ID
        _hash = get_hash

        rate = utils.get_subscription_rate(self.client)
        context["amount"] = rate
        return context


def bank(request):
    client = Client.objects.get(user=request.user)
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.client = client
            obj.save()
            messages.success(request, "Subscription was successful")
            return redirect("profile")
    else:
        form = SubscriptionForm()
    return render(
        request, "subscription/subscribe.html", {"object": client, "form": form}
    )
