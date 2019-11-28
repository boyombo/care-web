from django.contrib import admin

from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["amount", "payment_date", "reference", "status"]
    readonly_fields = ["amount", "payment_date", "reference", "status"]

    def has_delete_permission(self, request, obj=None):
        return False
