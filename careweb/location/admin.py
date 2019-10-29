from django.contrib import admin

from location.models import LGA


@admin.register(LGA)
class LGAAdmin(admin.ModelAdmin):
    list_display = ['name']
