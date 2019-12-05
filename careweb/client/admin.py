from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render

from client.models import HMO, Dependant, Client, Association, ClientAssociation
from ranger.models import Ranger
from subscription.utils import get_subscription_rate, create_subscription
from subscription.models import SubscriptionPayment


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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(primary__ranger__user=request.user)


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
    actions = ["subscribe_client"]
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

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True

    def subscribe_client(self, request, queryset):
        try:
            ranger = Ranger.objects.get(user=request.user)
        except Ranger.DoesNotExist:
            messages.error(request, "Sorry, you cannot subscriber for a client")
            return

        if queryset.count() != 1:
            messages.error(
                request, "Sorry, you can only subscribe one client at a time"
            )
            return

        client = queryset[0]
        rate = get_subscription_rate(client)
        if rate > ranger.balance:
            messages.error(
                request, "Sorry, you do not have enough balance for this subscription"
            )
            return

        if request.method == "POST" and "apply" in request.POST:
            ranger.balance -= rate
            ranger.save()
            create_subscription(client, rate)
            SubscriptionPayment.objects.create(
                client=client,
                amount=rate,
                status=SubscriptionPayment.SUCCESSFUL,
                ranger=ranger,
            )
            messages.success(request, "The subscription was successful")
        else:
            return render(
                request,
                "admin/client/subscribe.html",
                {"ranger": ranger, "client": client, "amount": rate},
            )

    def save_model(self, request, obj, form, change):
        try:
            ranger = Ranger.objects.get(user=request.user)
        except Ranger.DoesNotExist:
            pass
        else:
            # usr = obj.user
            # usr.active = True
            # usr.save()
            obj.ranger = ranger
            obj.save()
        super().save_model(request, obj, form, change)
