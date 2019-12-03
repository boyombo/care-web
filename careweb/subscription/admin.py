from django.contrib import admin
from django import forms

from subscription.models import Subscription, SubscriptionPayment


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
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


class PaymentForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPayment
        fields = ["client", "amount"]


@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = [
        "client",
        "payment_date",
        "amount",
        "bank",
        "status",
        "rejection_reason",
    ]
    search_fields = ["client__user__username", "client__first_name"]
    list_filter = ["status"]
    autocomplete_fields = ["client"]
    form = PaymentForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(ranger__user=request.user)
