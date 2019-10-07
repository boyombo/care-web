from django.contrib import admin

from client.models import CareProvider, Ranger, HMO, Dependant, Client


@admin.register(CareProvider)
class CareProviderAdmin(admin.ModelAdmin):
    list_display = ['code_no', 'name']


@admin.register(Ranger)
class RangerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone']


@admin.register(HMO)
class HMOAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Dependant)
class DependantAdmin(admin.ModelAdmin):
    list_display = ['surname', 'first_name', 'dob', 'designation']


class DependantInline(admin.TabularInline):
    model = Dependant


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['surname', 'first_name', 'dob', 'sex', 'pcp']
    inlines = [DependantInline]
