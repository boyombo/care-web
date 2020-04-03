from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from careweb.utils import HashIdFieldAdminMixin
from provider.models import CareProvider


@admin.register(CareProvider)
class CareProviderAdmin(HashIdFieldAdminMixin, SimpleHistoryAdmin):
    list_display = ['name', 'phone1', 'lga']
    list_filter = ['lga']
    search_fields = ['name']
