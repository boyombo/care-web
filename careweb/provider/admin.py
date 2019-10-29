from django.contrib import admin

from provider.models import CareProvider


@admin.register(CareProvider)
class CareProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone1', 'lga']
    list_filter = ['lga']
    search_fields = ['name']
