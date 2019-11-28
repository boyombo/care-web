from django.contrib import admin
from django.contrib import messages

from ranger.models import Ranger, WalletFunding
from payment.models import Payment


@admin.register(Ranger)
class RangerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "phone", "lga", "balance"]
    list_filter = ["lga"]
    search_fields = ["first_name", "last_name"]


@admin.register(WalletFunding)
class WalletFundingAdmin(admin.ModelAdmin):
    list_display = ["ranger", "amount", "bank", "status", "payment_date"]
    list_filter = ["status"]
    search_fields = ["ranger__first_name", "ranger__last_name", "ranger_phone"]
    date_hierarchy = "payment_date"
    actions = ["approve_funding"]
    readonly_fields = [
        "ranger",
        "amount",
        "payment_date",
        "bank",
        "name",
        "payment",
        "status",
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def approve_funding(modeladmin, request, queryset):
        count = 0
        for item in queryset:
            payment = item.payment
            if payment.status != Payment.PENDING:
                continue
            payment.status = Payment.SUCCESSFUL
            payment.save()

            item.status = WalletFunding.SUCCESSFUL
            item.save()

            ranger = item.ranger
            ranger.balance = item.amount
            ranger.save()
            count += 1
        if count > 0:
            messages.success(request, "Funding requests successful")
        else:
            messages.error(request, "Could not approve the request")
