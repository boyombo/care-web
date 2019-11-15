from django.contrib import admin

from core.models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "code",
        "client_rate",
        "spouse_dependant_rate",
        "minor_dependant_rate",
        "other_dependant_rate",
    ]
