from django.contrib import admin

from core.models import Plan, PlanRate


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "code",
        "has_extra",
    ]


@admin.register(PlanRate)
class PlanRateAdmin(admin.ModelAdmin):
    list_display = ["plan", "payment_cycle", "rate", "extra_rate", "has_extra"]
