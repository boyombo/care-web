from django.contrib import admin

from ranger.models import Ranger


@admin.register(Ranger)
class RangerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'lga']
    list_filter = ['lga']
    search_fields = ['first_name', 'last_name']
