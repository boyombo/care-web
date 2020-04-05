from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from careweb.utils import HashIdFieldAdminMixin
from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(HashIdFieldAdminMixin, SimpleHistoryAdmin):
    list_display = ["amount", "payment_date", "reference", "status"]
    readonly_fields = ["amount", "payment_date", "reference", "status"]

    def has_delete_permission(self, request, obj=None):
        return False
