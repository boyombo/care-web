from django.contrib import admin

from client.models import HMO, Dependant, Client, Association, ClientAssociation


@admin.register(HMO)
class HMOAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):
    list_display = ["name"]


class AssociationInline(admin.TabularInline):
    model = ClientAssociation
    extra = 1


@admin.register(Dependant)
class DependantAdmin(admin.ModelAdmin):
    list_display = ["surname", "first_name", "dob", "relationship"]


class DependantInline(admin.TabularInline):
    model = Dependant


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "surname",
        "first_name",
        "active",
        "package_option",
        "plan",
        "user",
        "verification_code",
    ]
    inlines = [DependantInline, AssociationInline]
    search_fields = ["user__username", "surname", "first_name"]
    autocomplete_fields = ["ranger", "pcp"]
    exclude = ["user"]
    fieldsets = [
        (
            "Basic",
            {
                "fields": ["surname", "first_name", "middle_name", "photo"],
                "classes": [
                    "baton-tabs-init",
                    "baton-tab-fs-personal",
                    "baton-tab-fs-contact",
                    "baton-tab-fs-ids",
                    "baton-tab-fs-work",
                    "baton-tab-fs-package",
                    "baton-tab-inline-dependant",
                    "baton-tab-inline-clientassociation",
                ],
            },
        ),
        (
            "Personal",
            {
                "fields": ["dob", "sex", "marital_status"],
                "classes": ["tab-fs-personal"],
            },
        ),
        (
            "Contact",
            {
                "fields": ["phone_no", "whatsapp_no", "email", "home_address"],
                "classes": ["tab-fs-contact"],
            },
        ),
        (
            "IDs",
            {
                "fields": [
                    "national_id_card_no",
                    "drivers_licence_no",
                    "lagos_resident_no",
                    "lashma_no",
                    "lashma_quality_life_no",
                ],
                "classes": ["tab-fs-ids"],
            },
        ),
        (
            "Work",
            {
                "fields": ["occupation", "company", "office_address",],
                "classes": ["tab-fs-work"],
            },
        ),
        (
            "Package",
            {
                "fields": ["plan", "payment_option", "payment_instrument",],
                "classes": ["tab-fs-package"],
            },
        ),
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(ranger__user=request.user)
