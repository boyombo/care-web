from django.contrib import admin

from client.models import CareProvider, Ranger, HMO, Dependant,\
    Client, Location, LGA


@admin.register(LGA)
class LGAAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'lga']


@admin.register(CareProvider)
class CareProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone1', 'lga']
    list_filter = ['lga']
    search_fields = ['name']


@admin.register(Ranger)
class RangerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'lga']
    list_filter = ['lga']
    search_fields = ['first_name', 'last_name']


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
    autocomplete_fields = ['ranger', 'pcp']
