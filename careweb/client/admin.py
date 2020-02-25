from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render

from client.forms import ClientAdminForm
from client.models import (
    HMO,
    Dependant,
    Client,
    Association,
    ClientAssociation,
    MyClient,
)
from client.utils import get_verification_code, phone_no_valid, is_registered_user, get_export_row
from core.utils import send_email
from constance import config
from ranger.models import Ranger
from subscription.utils import get_subscription_rate, create_subscription
from subscription.models import SubscriptionPayment
from client.admin_filters import MyClientFilter
import django_excel as excel


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


@admin.register(MyClient)
class MyClientAdmin(admin.ModelAdmin):
    list_display = [
        "surname",
        "first_name",
        "active",
        "payment_option",
        "plan",
        "subscription_rate",
        "verified",
    ]
    actions = ["subscribe_client"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True

    def subscribe_client(self, request, queryset):
        try:
            ranger = Ranger.objects.get(user=request.user)
        except Ranger.DoesNotExist:
            messages.error(request, "Sorry, you cannot subscribe for a client")
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


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'js/client_admin2.js',
        )

    form = ClientAdminForm
    list_display = [
        "surname",
        "first_name",
        "active",
        "payment_option",
        "plan",
        "subscription_rate",
        "user",
        "verification_code",
        "verified",
    ]
    inlines = [DependantInline, AssociationInline]
    search_fields = ["user__username", "surname", "first_name"]
    autocomplete_fields = ["ranger"]
    exclude = ["user"]
    readonly_fields = ["lashma_quality_life_no"]
    actions = ["subscribe_client", "verify_client", "export_clients"]
    list_filter = (MyClientFilter,)
    fieldsets = [
        (
            "Basic",
            {
                "fields": ["surname", "first_name", "middle_name", "photo"],
                "classes": [
                    "baton-tabs-init",
                    "baton-tab-fs-personal",
                    "baton-tab-fs-contact",
                    "baton-tab-fs-provider",
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
            "Provider",
            {
                "fields": ["lga", "pcp"],
                "classes": ["tab-fs-provider"],
            },
        ),
        (
            "IDs",
            {
                "fields": [
                    "national_id_card_no",
                    "drivers_licence_no",
                    "lagos_resident_no",
                    "voters_card_no",
                    "international_passport_no",
                    "lashma_no",
                    "lashma_quality_life_no",
                ],
                "classes": ["tab-fs-ids"],
            },
        ),
        (
            "Work",
            {
                "fields": ["occupation", "company", "office_address", ],
                "classes": ["tab-fs-work"],
            },
        ),
        (
            "Package",
            {
                "fields": ["plan", "payment_option", "payment_instrument", ],
                "classes": ["tab-fs-package"],
            },
        ),
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(ranger__user=request.user)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(ClientAdmin, self).get_form(request, obj, change, **kwargs)
        form.http_request = request
        return form

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True

    def get_actions(self, request):
        # import pdb;pdb.set_trace()
        actions = super().get_actions(request)
        if request.user.is_superuser:
            if "subscribe_client" in actions:
                del actions["subscribe_client"]
            return actions
        else:
            if "verify_client" in actions:
                del actions["verify_client"]
            return actions

    def verify_client(self, request, queryset):
        if request.user.is_superuser:
            queryset.update(verified=True)
        else:
            messages.error(request, "Sorry you cannot verify a client")

    def export_clients(self, request, queryset):
        column_names = [
            "S/N", "Salutation", "First Name", "Middle Name", "Last Name", "Date of Birth", "Phone Number",
            "Relationship", "Gender", "Premium for Principal", "State ID", "National ID", "Passport",
            "Staff ID", "Voter ID", "Driver's License", "Secondary Phone Number", "LGA/LCDA", "Preferred Provider Name",
            "Package", "Period", "LSHS Code", "QL Code"
        ]
        output = [column_names]
        rows = []
        index = 1
        for client in queryset:
            for row in get_export_row(client, index):
                index += 1
                rows.append(row)
        output.extend(rows)
        sheet = excel.pe.Sheet(output)
        return excel.make_response(sheet, "xls", file_name="Clients")

    def subscribe_client(self, request, queryset):
        try:
            ranger = Ranger.objects.get(user=request.user)
        except Ranger.DoesNotExist:
            messages.error(request, "Sorry, you cannot subscribe for a client")
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
        if not phone_no_valid(obj.phone_no, str(obj.id)):
            messages.error(request, "Phone no already in use")
            return
        try:
            ranger = Ranger.objects.get(user=request.user)
        except Ranger.DoesNotExist:
            pass
        else:
            # usr = obj.user
            # usr.active = True
            # usr.save()
            obj.ranger = ranger
            sub_rate = get_subscription_rate(obj)
            obj.subscription_rate = "{}".format(sub_rate)
            messages.success(request, "The subscription rate for {} is {}".format(obj.full_name, sub_rate))
        if obj.email and not is_registered_user(str(obj.id)):
            password = config.CLIENT_DEFAULT_PASSWORD
            usr = User.objects.create_user(username=obj.email, password=password, email=obj.email)
            code = get_verification_code()
            obj.user = usr
            obj.uses_default_password = True
            obj.verification_code_verified = False
            obj.verification_code = code
            context = {"name": obj.first_name, "code": code}
            send_email(obj.email, "welcome_app", context)
        elif obj.phone_no and not is_registered_user(str(obj.id)):
            password = config.CLIENT_DEFAULT_PASSWORD
            usr = User.objects.create_user(username=obj.phone_no, password=password)
            code = get_verification_code()
            obj.user = usr
            obj.uses_default_password = True
            obj.verification_code_verified = False
            obj.verification_code = code
        else:
            obj.verified = True
        obj.save()
        super().save_model(request, obj, form, change)
