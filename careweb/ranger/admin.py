from django.contrib import admin

from ranger.models import Ranger, WalletFunding


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
