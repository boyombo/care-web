from django.contrib import admin

from client.models import HMO, Dependant, Client, Association


@admin.register(HMO)
class HMOAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):
    list_display = ['name']


class AssociationInline(admin.TabularInline):
    model = Client.associations.through


@admin.register(Dependant)
class DependantAdmin(admin.ModelAdmin):
    list_display = ['surname', 'first_name', 'dob', 'relationship']


class DependantInline(admin.TabularInline):
    model = Dependant


# @admin.register(Client)
# class ClientAdmin(admin.ModelAdmin):
#     list_display = ['surname', 'first_name', 'dob', 'sex', 'pcp']
#     inlines = [DependantInline, AssociationInline]
#     autocomplete_fields = ['ranger', 'pcp']
#     exclude = ['associations']
