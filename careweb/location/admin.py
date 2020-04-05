from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from careweb.utils import HashIdFieldAdminMixin
from location.models import LGA


@admin.register(LGA)
class LGAAdmin(HashIdFieldAdminMixin, SimpleHistoryAdmin):
    list_display = ['name']
