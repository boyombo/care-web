from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from core.models import Plan, PlanRate


@admin.register(Plan)
class PlanAdmin(SimpleHistoryAdmin):
    list_display = ["name", "code", "has_extra", "family_inclusive", "size"]


@admin.register(PlanRate)
class PlanRateAdmin(SimpleHistoryAdmin):
    list_display = ["plan", "payment_cycle", "rate", "extra_rate", "has_extra"]
