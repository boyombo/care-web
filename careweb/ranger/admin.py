from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect

from ranger.models import Ranger, WalletFunding
from payment.models import Payment
from payment.utils import approve_funding
from ranger.forms import RejectForm


@admin.register(Ranger)
class RangerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "phone", "lga", "balance", "user"]
    list_filter = ["lga"]
    search_fields = ["first_name", "last_name"]


@admin.register(WalletFunding)
class WalletFundingAdmin(admin.ModelAdmin):
    list_display = [
        "ranger",
        "amount",
        "bank",
        "status",
        "payment_date",
        "reference",
        "rejection_reason",
    ]
    list_filter = ["status"]
    search_fields = ["ranger__first_name", "ranger__last_name", "ranger__phone"]
    date_hierarchy = "payment_date"
    actions = ["approve_funding", "reject_funding"]
    readonly_fields = ["ranger", "payment", "status", "rejection_reason"]
    # readonly_fields = [
    #    "ranger",
    #    "amount",
    #    "payment_date",
    #    "bank",
    #    "name",
    #    "payment",
    #    "status",
    # ]

    # def has_view_permission(self, request, obj=None):
    #    if obj and obj.ranger and request.user == obj.ranger.user:
    #        return True
    #    return False

    # def get_prepopulated_fields(self, request):
    #    usr = request.user
    #    try:
    #        ranger = Ranger.objects.get(user=usr)
    #    except Ranger.DoesNotExist:
    #        return []
    #    return

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.is_superuser:
            return actions
        return []

    def save_model(self, request, obj, form, change):
        try:
            ranger = Ranger.objects.get(user=request.user)
        except Ranger.DoesNotExist:
            obj.ranger = None
        else:
            pymt = Payment.objects.create(
                amount=obj.amount,
                reference="{}-{}".format(obj.name, obj.bank),
                status=Payment.PENDING,
            )
            obj.ranger = ranger
            obj.payment = pymt
            obj.save()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(ranger__user=request.user)

    def has_change_permission(self, request, obj=None):
        # import pdb; pdb.set_trace()
        if obj and obj.ranger and request.user == obj.ranger.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def approve_funding(modeladmin, request, queryset):
        count = 0
        for item in queryset:
            approve_funding(item)
            # payment = item.payment
            # if payment.status != Payment.PENDING:
            #    continue
            # payment.status = Payment.SUCCESSFUL
            # payment.save()

            # item.status = WalletFunding.SUCCESSFUL
            # item.save()

            # ranger = item.ranger
            # ranger.balance = item.amount
            # ranger.save()
            count += 1
        if count > 0:
            messages.success(request, "Funding requests successful")
        else:
            messages.error(request, "Could not approve the request")

    def reject_funding(self, request, queryset):
        # import pdb

        # pdb.set_trace()
        if queryset.count() > 1:
            messages.error(request, "You can only reject one request at a time")
            return

        funding_request = queryset[0]
        if funding_request.status != WalletFunding.PENDING:
            messages.error(request, "You can only reject a pending request")
            return

        if request.method == "POST":
            # import pdb;pdb.set_trace()
            form = RejectForm(request.POST)
            if form.is_valid() and "apply" in request.POST:
                _funding = WalletFunding.objects.get(
                    pk=request.POST["_selected_action"]
                )
                _funding.status = WalletFunding.FAILED
                _funding.rejection_reason = form.cleaned_data["reason"]
                _funding.save()
                return HttpResponseRedirect(request.get_full_path())
        else:
            form = RejectForm()

        return render(
            request,
            "admin/ranger/reject_funding.html",
            {"form": form, "funding": queryset[0]},
        )
