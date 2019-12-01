from django.contrib import admin

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
