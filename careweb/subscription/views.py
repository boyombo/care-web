from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.base import TemplateView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from client.models import Client
from ranger.models import Ranger
from subscription.forms import SubscriptionForm
from subscription.models import SubscriptionPayment
from payment.models import Payment
from payment.utils import get_reference
from subscription import utils
from core.crypto import Encryptor, get_hash
from django.conf import settings

from subscription.serializers import CreateSubscriptionSerializer, SubscriptionPaymentSerializer


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


class CreateSubscriptionPayment(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = CreateSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            ranger = None
            if data.get('ranger_id'):
                ranger = Ranger.objects.get(id=data.get('ranger_id'))
            client = Client.objects.get(id=data.get('client_id'))
            sp = SubscriptionPayment.objects.create(client=client, amount=data.get('amount'), bank=data.get('bank'),
                                                    name=data.get('name'), payment_type=data.get('payment_type'),
                                                    ranger=ranger)
            serialized = SubscriptionPaymentSerializer(sp)
            return Response({"success": True, "subscription": serialized.data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_200_OK)


class GetSubscriptionPaymentsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, ranger_id, format=None):
        if Ranger.objects.filter(id=ranger_id).exists():
            payments = SubscriptionPayment.objects.filter(ranger=Ranger.objects.get(id=ranger_id))
            serialized = SubscriptionPaymentSerializer(payments, many=True)
            return Response({"success": True, "payments": serialized.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False,
                             'message': 'No such ranger'},
                            status=status.HTTP_200_OK)
