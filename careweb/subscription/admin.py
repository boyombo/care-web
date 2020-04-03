from django import forms

from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render
from simple_history.admin import SimpleHistoryAdmin

from client.models import Client
from subscription.models import Subscription, SubscriptionPayment, Commission
from subscription.utils import get_subscription_rate, create_subscription


@admin.register(Commission)
class CommissionAdmin(SimpleHistoryAdmin):
    list_display = ["subscription", "amount", "subscription_amount", "ranger", "when"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(ranger__user=request.user)


@admin.register(Subscription)
class SubscriptionAdmin(SimpleHistoryAdmin):
    list_display = [
        "client",
        "subscribed_on",
        "expiry_date",
        "plan",
        "amount",
        "active",
    ]
    search_fields = ["client__user__username", "client_first_name"]
    list_filter = ["active"]
    readonly_fields = [
        "start_date",
        "next_subscription",
        "dependants",
        "client",
        "subscribed_on",
        "expiry_date",
        "plan",
        "amount",
        "active",
    ]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPayment
        fields = ["client", "amount"]


@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(SimpleHistoryAdmin):
    list_display = [
        "client",
        "payment_date",
        "amount",
        "bank",
        "name",
        "status",
        "rejection_reason",
    ]
    search_fields = ["client__user__username", "client__first_name"]
    list_filter = ["status"]
    autocomplete_fields = ["client"]
    form = PaymentForm
    readonly_fields = ["client", "amount"]
    actions = ["approve_subscription"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(ranger__user=request.user)

    def approve_subscription(self, request, queryset):
        if queryset.count() != 1:
            messages.error(request, "Sorry, you can only approve one client at a time")
            return

        sub = queryset[0]
        create_subscription(sub.client, sub.amount)
        sub.status = SubscriptionPayment.SUCCESSFUL
        sub.save()
        messages.success(request, "The subscription was successful")
