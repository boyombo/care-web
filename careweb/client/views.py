# from pprint import pprint
from random import sample
from decimal import Decimal

from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView

# from django.urls import reverse_lazy

from client.models import Client, Dependant, ClientAssociation, Association
from core.utils import send_welcome_email, send_email
from subscription.utils import get_subscription_rate, create_subscription
from payment.utils import get_reference
from client.utils import get_client_details
from ranger.models import Ranger

# from client.models import Plan
from client.forms import (
    RegForm,
    ApiRegForm,
    LoginForm,
    PersonalInfoForm,
    AssociationsForm,
    DependantForm,
    PhotoForm,
    AmountForm,
)

import logging

logger = logging.getLogger(__name__)


@login_required
def profile(request, pk=None):
    if pk:
        client = Client.objects.get(pk=pk)
    else:
        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            return redirect("login")
    subscription_rate = get_subscription_rate(client)
    return render(
        request,
        "client/profile.html",
        {"profile": client, "subscription_rate": subscription_rate},
    )


def register(request):
    if request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data["password"]
            username = form.cleaned_data["email"]

            new_user = User.objects.create_user(username=username, password=pwd)

            client = form.save(commit=False)
            client.user = new_user
            client.email = username
            client.save()
            _user = authenticate(username=username, password=pwd)
            if _user:
                send_welcome_email(username, client.first_name)
                login(request, _user)
                return redirect("profile", pk=client.id)
            else:
                return redirect("login")
    else:
        form = RegForm()
    return render(request, "client/register.html", {"form": form})


def client_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # import pdb;pdb.set_trace()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            login(request, user)

            # A client?
            try:
                cl = Client.objects.get(user=request.user)
            except Client.DoesNotExist:
                return redirect("/admin/")
            else:
                return redirect("profile", pk=cl.id)
    else:
        form = LoginForm()
    return render(request, "client/login.html", {"form": form})


class ClientView(UpdateView):
    model = Client


class PlanView(ClientView):
    fields = ["plan", "payment_option", "payment_instrument"]
    template_name = "client/plan.html"


class PersonalInfoView(ClientView):
    form_class = PersonalInfoForm
    template_name = "client/personal.html"


class ContactView(ClientView):
    fields = ["phone_no", "whatsapp_no", "home_address"]
    template_name = "client/contact.html"


class WorkView(ClientView):
    fields = ["occupation", "company", "office_address"]
    template_name = "client/work.html"


class PCPView(ClientView):
    fields = ["pcp"]
    template_name = "client/pcp.html"


def associations(request, pk):
    client = get_object_or_404(Client, pk=pk)
    my_associations = ClientAssociation.objects.filter(client=client)
    init = {"associations": [i.association.id for i in my_associations]}
    if request.method == "POST":
        form = AssociationsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["associations"]
            my_associations.delete()
            for item in data:
                _association = Association.objects.get(pk=item)
                ClientAssociation.objects.create(
                    client=client, association=_association
                )
            return redirect("profile", pk=client.id)
    else:
        form = AssociationsForm(initial=init)
    return render(request, "client/associations.html", {"form": form, "object": client})


class AssociationsView(ClientView):
    template_name = "client/associations.html"
    form_class = AssociationsForm

    def form_valid(self, form):
        response = super().form_valid(form)
        associations = form.cleaned_data["associations"]
        for association in associations:
            ClientAssociation.objects.get_or_create(
                client=self.object, association=association
            )
        return response


def dependants(request, pk):
    client = Client.objects.get(pk=pk)
    _deps = Dependant.objects.filter(primary=client)
    return render(
        request, "client/dependants.html", {"object": client, "dependants": _deps}
    )


def add_dependant(request):
    client = Client.objects.get(user=request.user)
    if request.method == "POST":
        form = DependantForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.primary = client
            obj.save()
            messages.info(request, "Dependant added successfully")
            return redirect("profile_dependants", pk=client.id)
    else:
        form = DependantForm()
    return render(
        request, "client/add_dependant.html", {"form": form, "object": client}
    )


## Endpoints


@csrf_exempt
def register_api(request):
    if request.method == "POST":
        logger.info("signing up...")
        form = ApiRegForm(request.POST)
        logger.info(form.data)
        if form.is_valid():
            logger.info(form.cleaned_data)
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            usr = User.objects.create_user(
                username=email, password=password, email=email
            )
            logger.info("created user")
            usr.is_active = False
            usr.save()
            # create verification code
            code = "".join(sample("0123456789", 5))
            logger.info("code is {}".format(code))

            obj = form.save(commit=False)
            obj.user = usr
            obj.verification_code = code
            obj.save()
            # send verification code in email
            context = {"name": obj.first_name, "code": code}
            logger.info("context {}".format(context))
            send_email(email, "welcome_app", context)

            return JsonResponse(
                {
                    "success": True,
                    "client": {
                        "active": usr.is_active,
                        "id": obj.id.hashid,
                        "surname": obj.surname,
                        "firstName": obj.first_name,
                        "email": obj.email,
                        "phone": obj.phone_no,
                        "photo": "",
                    },
                }
            )
    return JsonResponse({"success": False})


@csrf_exempt
def login_api(request):
    # import pdb; pdb.set_trace()
    if request.method == "POST":
        logger.info("logging in...")
        form = LoginForm(request.POST)
        logger.info("form {}".format(form.data))
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            logger.info("form {}".format(form.cleaned_data))

            usr = authenticate(username=username, password=password)
            if usr is not None:
                try:
                    client = Client.objects.get(user=usr)
                except Client.DoesNotExist:
                    return HttpResponseBadRequest(
                        "Please contact support. Your account is not configured correctly"
                    )
                    # return JsonResponse(
                    #    {
                    #        "error": "Please contact support, your account is not configured correctly",
                    #        "success": False,
                    #    }
                    # )
                else:
                    host = "https://{}".format(request.get_host())
                    logger.info("client details")
                    client_details = get_client_details(client, host)
                    logger.info(client_details)
                    return JsonResponse({"success": True, "client": client_details})
                    # if client.photo:
                    #    photo_url = "{}{}".format(host, client.photo.url)
                    # else:
                    #    photo_url = ""
                    # if client.dob:
                    #    dob = client.dob.strftime("%Y-%m-%d")
                    # else:
                    #    dob = None
                    # dependants = [
                    #    {
                    #        "dob": dependant.dob.strftime("%Y-%m-%d"),
                    #        "first_name": dependant.first_name,
                    #        "surname": dependant.surname,
                    #        "middle_name": dependant.middle_name,
                    #        "relationship": dependant.relationship,
                    #        "pcp": dependant.pcp.id.id if dependant.pcp else None,
                    #    }
                    #    for dependant in Dependant.objects.filter(primary=client)
                    # ]
                    # subscription_rate = get_subscription_rate(client)
                    # return JsonResponse(
                    #    {
                    #        "client": {
                    #            "active": client.user.is_active,
                    #            "subscription_rate": subscription_rate,
                    #            "id": client.id.id,
                    #            "surname": client.surname,
                    #            "firstName": client.first_name,
                    #            "phone": client.phone_no,
                    #            "whatsapp": client.whatsapp_no,
                    #            "email": client.email,
                    #            "imageUri": photo_url,
                    #            "dob": dob,
                    #            "sex": client.sex,
                    #            "maritalStatus": client.marital_status,
                    #            "nationalIdNo": client.national_id_card_no,
                    #            "driversLicenceNo": client.drivers_licence_no,
                    #            "lagosResidentsNo": client.lagos_resident_no,
                    #            "lashmaNo": client.lashma_no,
                    #            "lashmaQualityLifeNo": client.lashma_quality_life_no,
                    #            "pcp": client.pcp.id.id if client.pcp else None,
                    #            "ranger": client.ranger.id.id
                    #            if client.ranger
                    #            else None,
                    #            "homeAddress": client.home_address,
                    #            "occupation": client.occupation,
                    #            "company": client.company,
                    #            "officeAddress": client.office_address,
                    #            "packageOption": client.package_option,
                    #            "plan": client.plan.id if client.plan else None,
                    #            "paymentOption": client.payment_option,
                    #            "paymentInstrument": client.payment_instrument,
                    #            "dependants": dependants,
                    #        },
                    #        "success": True,
                    #    }
                    # )
        else:
            logger.info(form.errors)
            return HttpResponseBadRequest(
                "Please contact support. Your account is not configured correctly"
            )
            # return JsonResponse(
            #    {
            #        "success": False,
            #        "message": "Please check your username and password then try again",
            #    }
            # )


@csrf_exempt
def upload_photo(request, id):
    logger.info("starting client  upload")
    cl = get_object_or_404(Client, pk=id)
    # import pdb;pdb.set_trace()
    logger.info("got client for photo upload")
    # pprint("got client")
    logger.info(cl)
    # pprint(cl)
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES, instance=cl)
        logger.info("photo form")
        logger.info(form)
        logger.info("files")
        logger.info(request.FILES)
        # pprint(form)
        if form.is_valid():
            logger.info("photo-form is valid")
            form.save()
            host = "https://{}".format(request.get_host())
            if cl.photo:
                photo_url = "{}{}".format(host, cl.photo.url)
            else:
                photo_url = ""
        else:
            errors = form.errors
            logger.info("photo errors")
            logger.info(errors)
            return JsonResponse({"success": False})
        return JsonResponse(
            {
                "client": {
                    "id": cl.id,
                    "surname": cl.surname,
                    "firstName": cl.first_name,
                    "phone": cl.phone_no,
                    "email": cl.email,
                    "photo": photo_url,
                },
                "success": True,
            }
        )


def get_client_photo(request, id):
    cl = get_object_or_404(Client, pk=id)
    host = "https://{}".format(request.get_host())
    if cl.photo:
        photo_url = "{}{}".format(host, cl.photo.url)
    else:
        photo_url = ""
    return JsonResponse({"success": True, "imageUri": photo_url})


def verify_code(request):
    code = request.GET.get("code")
    id = request.GET.get("id")
    try:
        cl = Client.objects.get(pk=id)
    except Client.DoesNotExist:
        return JsonResponse({"success": False, "error": "User does not exist"})

    usr = cl.user
    if not usr:
        return JsonResponse({"success": False, "error": "User not configured properly"})
    # if usr.is_active:
    #    return JsonResponse({"success": True})
    if code == cl.verification_code:
        usr.is_active = True
        usr.save()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "Wrong code"})


def get_clients(request, id):
    host = "https://{}".format(request.get_host())
    ranger = get_object_or_404(Ranger, pk=id)
    clients = [
        get_client_details(cl, host) for cl in Client.objects.filter(ranger=ranger)
    ]
    return JsonResponse({"success": True, "clients": clients})


@csrf_exempt
def create_client_subscription(request, client_id, ranger_id):
    client = get_object_or_404(Client, pk=client_id)
    ranger = get_object_or_404(Ranger, pk=ranger_id)
    if request.method == "POST":
        form = AmountForm(request.POST)
        if form.is_valid():
            amount = Decimal(form.cleaned_data["amount"])
            sub = create_subscription(client, amount)
            if sub:
                # deduct from ranger balance
                ranger.balance -= amount
                ranger.save()
                return JsonResponse({"success": True, "newBalance": ranger.balance})
    return JsonResponse({"success": False})


def payment(request, id):
    client = Client.objects.get(user=request.user)
    return render(request, "client/payment.html", {"client": client})


#    cl = get_object_or_404(Client, pk=id)
#    amount = get_subscription_rate(cl)
#    email = cl.email
#    merchant_id = settings.PAYGATE_MERCHANT_ID
#    curr_code = "566"
#    order_id = get_reference()
#    product = "Futurecare Subscription"
