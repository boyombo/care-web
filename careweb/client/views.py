# from pprint import pprint
from datetime import datetime
from random import sample
from decimal import Decimal
import base64

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.conf import settings
from django.core.files.base import ContentFile

# from django.urls import reverse_lazy

from client.models import Client, Dependant, ClientAssociation, Association, TempClientUpload
from core.models import Plan
from core.utils import send_welcome_email, send_email
from subscription.models import SubscriptionPayment
from subscription.utils import (
    get_subscription_rate,
    create_subscription,
    get_next_subscription_date,
)
from payment.utils import get_reference
from client.utils import (
    get_client_details,
    get_quality_life_number,
    get_verification_code,
    get_username_for_auth, is_registered_user)
from ranger.models import Ranger
from location.models import LGA
from provider.models import CareProvider
from constance import config

# from client.models import Plan
from client.forms import (
    RegForm,
    ApiRegForm,
    BasicRegForm,
    LoginForm,
    PersonalInfoForm,
    AssociationsForm,
    DependantForm,
    PhotoForm,
    AmountForm,
    PlanForm,
    PCPForm,
    ClientForm,
    ChangePasswordForm,
)

import logging

logger = logging.getLogger(__name__)


@login_required
def profile(request, pk=None):
    if pk:
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return redirect("login")
        else:
            if client.user != request.user:
                return redirect("login")
    else:
        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            return redirect("login")
    subscription_rate = get_subscription_rate(client)
    next_subscription = get_next_subscription_date(client)
    return render(
        request,
        "client/profile.html",
        {
            "profile": client,
            "subscription_rate": subscription_rate,
            "next_subscription": next_subscription,
        },
    )


def register(request):
    if request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data["password"]
            username = form.cleaned_data["email"]

            new_user = User.objects.create_user(username=username, password=pwd)
            # new_user.is_active = False
            new_user.save()
            # import pdb

            # pdb.set_trace()

            client = form.save(commit=False)
            client.user = new_user
            client.email = username
            # client.lashma_quality_life_no = get_quality_life_number()
            client.save()
            client.lashma_quality_life_no = get_quality_life_number(client)
            client.save()
            send_welcome_email(username, client.first_name)
            return redirect("post_register")
            # _user = authenticate(username=username, password=pwd)
            # if _user:
            #    # login(request, _user)
            #    # return redirect("profile", pk=client.id)
            #    return redirect("login")
            # else:
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
            un = get_username_for_auth(username)  # Enables authentication with phone no
            user = authenticate(username=un, password=password)
            login(request, user)

            # A client?
            try:
                cl = Client.objects.get(user=request.user)
                if not cl.verified:
                    return HttpResponseRedirect(reverse("verify_account"))
                if cl.uses_default_password:
                    messages.warning(
                        request, "You must change your password to proceed"
                    )
                    return HttpResponseRedirect(reverse("change_default_password"))
            except Client.DoesNotExist:
                return redirect("/admin/")
            else:
                return redirect("profile", pk=cl.id)
    else:
        form = LoginForm()
    return render(request, "client/login.html", {"form": form})


@login_required
def verify_code_web(request):
    if request.method == "GET":
        messages.success(
            request, "Supply the verification code sent to your email to proceed"
        )
    if request.method == "POST":
        code = request.POST.get("code")
        client = Client.objects.get(user=request.user)
        if client.verification_code == code:
            client.verified = True
            client.save()
            messages.success(request, "Account verification was successful")
            if client.uses_default_password:
                messages.warning(
                    request, "You need to change your password to proceed."
                )
                return HttpResponseRedirect(reverse("change_default_password"))
            return redirect("profile", pk=client.id)
        messages.error(request, "Invalid code supplied")
    return render(request, "client/verify_code.html")


@login_required
def change_default_password(request):
    form = ChangePasswordForm
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("new_password")
            user = request.user
            user.set_password(password)
            user.is_active = True
            user.save()
            client = Client.objects.get(user=user)
            client.uses_default_password = False
            client.verified = True
            client.save()
            messages.success(
                request,
                "Your password was changed successfully. You can now login with your new password",
            )
            logout(request)
            return HttpResponseRedirect(reverse("login"))
        messages.error(request, "One or more field empty")
    return render(request, "registration/change_default_password.html", {"form": form})


class ClientView(UpdateView):
    model = Client

    def get(self, request, pk):
        # import pdb;pdb.set_trace()
        try:
            _client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return redirect("login")

        if _client.user != request.user:
            raise PermissionDenied
            # return redirect("login")
        else:
            return super().get(request, pk)


def update_plan(request):
    client = Client.objects.get(user=request.user)
    if request.method == "POST":
        # form = PlanForm(request.POST)
        form = PlanForm(request.POST, instance=client)
        if form.is_valid():
            client.plan = form.cleaned_data["plan"]
            client.payment_option = form.cleaned_data["payment_option"]
            client.payment_instrument = form.cleaned_data["payment_instrument"]
            client.save()
            # import pdb;pdb.set_trace()
            # form.save()
    else:
        # form = PlanForm()
        form = PlanForm(instance=client)
    return render(request, "client/plan.html", {"form": form, "object": client})


class PlanView(ClientView):
    # form_class = PlanForm
    fields = ["plan", "payment_option", "payment_instrument"]
    template_name = "client/plan.html"


class IdentificationView(ClientView):
    fields = [
        "national_id_card_no",
        "drivers_licence_no",
        "lagos_resident_no",
        "lashma_no",
        "international_passport_no",
        "voters_card_no",
        # "lashma_quality_life_no",
    ]
    template_name = "client/identification.html"


class PersonalInfoView(ClientView):
    form_class = PersonalInfoForm
    template_name = "client/personal.html"


class PhotoView(ClientView):
    fields = ["photo"]
    template_name = "client/photo.html"


class ContactView(ClientView):
    fields = ["phone_no", "whatsapp_no", "home_address"]
    template_name = "client/contact.html"

    def form_valid(self, form):
        phone = form.cleaned_data.get('phone_no')
        if phone:
            if Client.objects.filter(phone_no=phone).exists():
                user = self.request.user
                if not user or not Client.objects.filter(user=user).exists():
                    form.add_error("phone_no", "Phone no has already been used")
                    messages.error(self.request, "Phone no has already been used")
                    return super(ContactView, self).form_invalid(form)
                client = Client.objects.get(user=user)
                if client.phone_no != phone:
                    form.add_error("phone_no", "Supplied phone no has already been used")
                    messages.error(self.request, "Supplied phone no has already been used")
                    return super(ContactView, self).form_invalid(form)
        return super(ContactView, self).form_valid(form)


class WorkView(ClientView):
    fields = ["occupation", "company", "office_address"]
    template_name = "client/work.html"


def load_pcp_list(request):
    lga_id = request.GET.get("lga")
    lga = LGA.objects.get(pk=lga_id)
    providers = CareProvider.objects.filter(lga=lga)
    return render(request, "client/provider_list.html", {"providers": providers})


class PCPView(ClientView):
    form_class = PCPForm
    # fields = ["pcp"]
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
        form = DependantForm(request.POST, request.FILES, primary=client)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.primary = client
            obj.save()
            messages.info(request, "Dependant added successfully")
            return redirect("profile_dependants", pk=client.id)
    else:
        form = DependantForm(primary=client)
    return render(
        request, "client/add_dependant.html", {"form": form, "object": client}
    )


def edit_dependant(request, pk):
    dependant = get_object_or_404(Dependant, pk=pk)
    client = dependant.primary
    if request.method == "POST":
        form = DependantForm(
            request.POST, request.FILES, instance=dependant, primary=client
        )
        if form.is_valid():
            print(dependant)
            dependant = form.save(commit=False)
            dependant.save()
            messages.info(request, "Dependant updated successfully")
            return redirect("profile_dependants", pk=client.id)
    else:
        form = DependantForm(instance=dependant, primary=client)
    return render(
        request, "client/edit_dependant.html", {"form": form, "object": client},
    )


def remove_dependant(request, pk):
    dependant = get_object_or_404(Dependant, pk=pk)
    client = dependant.primary
    if request.method == "POST":
        dependant.delete()
        return redirect("profile_dependants", pk=client.id)
    else:
        return render(
            request,
            "client/remove_dependant.html",
            {"dependant": dependant, "object": client},
        )


## Endpoints


@csrf_exempt
def register_via_agent(request, id):
    logger.info("request in for ranger with pk {}".format(id))
    ranger = get_object_or_404(Ranger, pk=id)
    if request.method == "POST":
        form = BasicRegForm(request.POST)
        if form.is_valid():
            cl = form.save()  # has to be committed to get QL number
            ranger = ranger
            cl.ranger = ranger
            cl.lashma_quqlity_life_no = get_quality_life_number(cl)
            cl.save()
            email = form.cleaned_data.get('email')
            phone_no = form.cleaned_data.get('phone_no')
            first_name = form.cleaned_data.get('first_name')
            if email and not is_registered_user(str(cl.id)):
                password = config.CLIENT_DEFAULT_PASSWORD
                usr = User.objects.create_user(username=email, password=password, email=email)
                code = get_verification_code()
                cl.user = usr
                cl.uses_default_password = True
                cl.verification_code_verified = False
                cl.verification_code = code
                context = {"name": first_name, "code": code}
                send_email(email, "welcome_app", context)
            elif phone_no and not is_registered_user(str(cl.id)):
                password = config.CLIENT_DEFAULT_PASSWORD
                usr = User.objects.create_user(username=phone_no, password=password)
                code = get_verification_code()
                cl.user = usr
                cl.uses_default_password = True
                cl.verification_code_verified = False
                cl.verification_code = code
            else:
                cl.verified = True
            cl.save()
            return JsonResponse(
                {
                    "success": True,
                    "client": {
                        "active": cl.verified,
                        "id": cl.id.id,
                        "surname": cl.surname,
                        "firstName": cl.first_name,
                        "email": cl.email,
                        "phone": cl.phone_no,
                        "photo": "",
                    },
                }
            )
        else:
            error_msg = form.errors.as_text()
            logger.info(error_msg)
            logger.info(form.errors)
            return HttpResponseBadRequest(error_msg)
            # return JsonResponse({"success": False, "error": error_msg})
    return HttpResponseBadRequest("Could not save client")
    # return JsonResponse({"success": False})


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
            # usr.is_active = False
            # usr.save()
            # create verification code
            # code = "".join(sample("0123456789", 5))
            code = get_verification_code()
            logger.info("code is {}".format(code))

            obj = form.save(commit=False)
            obj.user = usr
            obj.verification_code = code
            # obj.lashma_quality_life_no = get_quality_life_number()
            obj.verified = False
            obj.save()
            obj.lashma_quality_life_no = get_quality_life_number(obj)
            obj.save()
            # send verification code in email
            context = {"name": obj.first_name, "code": code}
            logger.info("context {}".format(context))
            send_email(email, "welcome_app", context)

            return JsonResponse(
                {
                    "success": True,
                    "client": {
                        "active": obj.verified,
                        "id": obj.id.id,
                        "surname": obj.surname,
                        "firstName": obj.first_name,
                        "email": obj.email,
                        "phone": obj.phone_no,
                        "photo": "",
                    },
                }
            )
        else:
            error_msg = form.errors.as_text().split("*")[-1]
            logger.info(error_msg)
            return JsonResponse({"success": False, "error": error_msg})
    return JsonResponse({"success": False})


@csrf_exempt
def login_api(request):
    # import pdb

    # pdb.set_trace()
    if request.method == "POST":
        logger.info("logging in...")
        form = LoginForm(request.POST)
        logger.info("form {}".format(form.data))
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            logger.info("form {}".format(form.cleaned_data))
            un = get_username_for_auth(username)  # Enables authentication with phone no
            usr = authenticate(username=un, password=password)
            logger.info("authenticated")
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
                    return JsonResponse({"success": True, "client": client_details, })
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

        host = "https://{}".format(request.get_host())
        details = get_client_details(cl, host)
        return JsonResponse({"success": True, "client": details})


@csrf_exempt
def upload_photo_b64(request, id):
    """upload photo as base64 string"""
    logger.info("uploading photo as base64")
    cl = get_object_or_404(Client, pk=id)
    # import pdb;pdb.set_trace()
    logger.info("got client for photo upload")
    # pprint("got client")
    logger.info(cl)
    if request.method == "POST":
        logger.info(request.body)
        logger.info(request.POST.__dict__)
        logger.info(request.POST)
        fd = request.body.decode("utf-8")
        fmt, imgstr = fd.split(";base64,")
        ext = fmt.split("/")[-1]
        file_name = "pic{}.{}".format(cl.id, ext)
        logger.info("fiile name: {}".format(file_name))
        data = ContentFile(base64.b64decode(imgstr))
        cl.photo.save(file_name, data, save=True)
        logging.info(cl.photo.url)
        photo_url = "https://" + request.get_host() + cl.photo.url
    return JsonResponse({"success": True, "image": photo_url})


def get_client_photo(request, id):
    cl = get_object_or_404(Client, pk=id)
    host = "https://{}".format(request.get_host())
    if cl.photo:
        photo_url = "{}{}".format(host, cl.photo.url)
    else:
        photo_url = ""
    return JsonResponse({"success": True, "imageUri": photo_url})


def verify_code(request):
    logger.info("verifying code...")
    code = request.GET.get("code")
    id = request.GET.get("id")
    logger.info("code is {}".format(code))
    logger.info("id is {}".format(id))
    try:
        cl = Client.objects.get(pk=id)
    except Client.DoesNotExist:
        return JsonResponse({"success": False, "error": "User does not exist"})

    logger.info("client seen")
    usr = cl.user
    if not usr:
        return JsonResponse({"success": False, "error": "User not configured properly"})
    # if usr.is_active:
    #    return JsonResponse({"success": True})
    if code == cl.verification_code:
        cl.verified = True
        cl.save()

        logger.info("verified code")
        usr.is_active = True
        usr.save()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "Wrong code"})


def get_client_info(request, id):
    client = get_object_or_404(Client, pk=id)
    host = "https://{}".format(request.get_host())
    details = get_client_details(client, host)
    return JsonResponse({"success": True, "client": details})


def get_clients(request, id):
    host = "https://{}".format(request.get_host())
    ranger = get_object_or_404(Ranger, pk=id)
    clients = [
        get_client_details(cl, host) for cl in Client.objects.filter(ranger=ranger)
    ]
    return JsonResponse({"success": True, "clients": clients})


@csrf_exempt
def create_client_subscription(request, client_id, ranger_id):
    logger.info("creating client subscription")
    client = get_object_or_404(Client, pk=client_id)
    logger.info("client is {}".format(client))
    ranger = get_object_or_404(Ranger, pk=ranger_id)
    logger.info("ranger is {}".format(ranger))
    if request.method == "POST":
        logger.info("post method called")
        form = AmountForm(request.POST)
        logger.info("form: {}".format(form.data))
        if form.is_valid():
            amount = Decimal(form.cleaned_data["amount"])
            sub = create_subscription(client, amount)
            logger.info("subscription info: {}".format(sub))
            if sub:
                # deduct from ranger balance
                ranger.balance -= amount
                ranger.save()

                # create subscription payment
                SubscriptionPayment.objects.create(
                    client=client,
                    ranger=ranger,
                    amount=amount,
                    name=client.full_name,
                    status=SubscriptionPayment.SUCCESSFUL,
                    payment_type=SubscriptionPayment.AGENT,
                )
                return JsonResponse({"success": True, "newBalance": ranger.balance})
    return JsonResponse({"success": False})


def add_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            host = "https://{}".format(request.get_host())
            ranger = get_object_or_404(Ranger, pk=id)
            clients = [
                get_client_details(cl, host)
                for cl in Client.objects.filter(ranger=ranger)
            ]
            return JsonResponse({"success": True, "clients": clients})
        else:
            return JsonResponse({"success": False})


def payment(request):
    client = Client.objects.get(user=request.user)
    return render(request, "client/payment.html", {"object": client})


#    cl = get_object_or_404(Client, pk=id)
#    amount = get_subscription_rate(cl)
#    email = cl.email
#    merchant_id = settings.PAYGATE_MERCHANT_ID
#    curr_code = "566"
#    order_id = get_reference()
#    product = "Futurecare Subscription"


def get_lga_pcp(request):
    lga = request.GET.get("lga")
    if lga:
        pcp_set = CareProvider.objects.filter(lga__id=lga)
        pcps = [
            {
                "id": str(pcp.id),
                "text": "{name} -- {address}".format(
                    name=pcp.name, address=pcp.address
                ),
            }
            for pcp in pcp_set
        ]
        return JsonResponse({"pcps": pcps})
    return JsonResponse({"pcps": []})


def get_pcp_lga(request):
    pcp = request.GET.get("pcp")
    if pcp:
        provider = CareProvider.objects.get(id=pcp)
        return JsonResponse({"id": str(provider.lga.id), "text": provider.lga.name})
    return JsonResponse({})


def upload_clients(request):
    if not request.FILES.get('file'):
        messages.error(request, "Invalid file selected")
        return JsonResponse({'status': 'error', 'info': 'Invalid file selected'})
    try:
        TempClientUpload.objects.all().delete()
        request.FILES.get('file').save_to_database(
            model=TempClientUpload,
            mapdict=[
                "s_no",
                "salutation",
                "first_name",
                "middle_name",
                "last_name",
                "dob",
                "phone_no",
                "relationship",
                "gender",
                "premium",
                "state_id",
                "national_id",
                "passport",
                "staff_id",
                "voter_id",
                "drivers_license",
                "secondary_phone_no",
                "lga",
                "provider",
                "package",
                "period",
                "lshs_code",
                "ql_code",
            ]
        )
        total = TempClientUpload.objects.count()
        valid = 0
        duplicate_no = 0
        relationship = {
            "Spouse": 0,
            "Daughter": 1,
            "Son": 2,
            "Others": 3
        }
        primary = None
        for item in TempClientUpload.objects.all():
            if not item.first_name or not item.last_name:
                continue
            else:
                ranger = Ranger.objects.get(user=request.user)
                try:
                    dob = datetime.strptime(item.dob.strip(), "%Y-%m-%d")
                except Exception as e:
                    dob = None
                try:
                    sex = item.gender.strip()[0].upper() if item.gender else ''
                    if item.relationship.title() == "Principal":
                        if not item.phone_no:
                            primary = None
                            continue
                        if Client.objects.filter(phone_no=item.phone_no.strip()).exists() or User.objects.filter(
                                username=item.phone_no.strip()):
                            duplicate_no += 1
                            primary = None
                            continue
                        try:
                            pcp = CareProvider.objects.get(name__iexact=item.provider.strip())
                        except Exception as e:
                            pcp = None
                        try:
                            lga = LGA.objects.get(name__iexact=item.lga.strip())
                        except:
                            lga = None
                        try:
                            plan = Plan.objects.get(name__iexact=item.package.strip())
                        except:
                            plan = None
                        client = Client.objects.create(first_name=item.first_name, surname=item.last_name,
                                                       middle_name=item.middle_name, sex=sex, dob=dob,
                                                       phone_no=item.phone_no, lagos_resident_no=item.state_id,
                                                       national_id_card_no=item.national_id,
                                                       international_passport_no=item.passport,
                                                       voters_card_no=item.voter_id,
                                                       pcp=pcp, ranger=ranger, lga=lga, subscription_rate=item.premium,
                                                       plan=plan, payment_option=item.period,
                                                       drivers_licence_no=item.drivers_license)
                        user = User.objects.create_user(username=item.phone_no.strip(),
                                                        password=config.CLIENT_DEFAULT_PASSWORD)
                        client.user = user
                        client.uses_default_password = True
                        client.lashma_quality_life_no = get_quality_life_number(client)
                        client.save()
                        primary = client
                    elif primary:
                        Dependant.objects.create(primary=primary, first_name=item.first_name, surname=item.last_name,
                                                 middle_name=item.middle_name, dob=dob,
                                                 relationship=relationship.get(item.relationship.strip().title()))
                    valid += 1
                except Exception as e:
                    print(e)
                    pass
        messages.success(request,
                         "Clients data successfully processed. {valid} clients were "
                         "created out of a total of {total}. {duplicate} records uses duplicate phone no".format(
                             valid=valid, total=total, duplicate=duplicate_no))
        TempClientUpload.objects.all().delete()
    except Exception as e:
        print(e)
        messages.error(request,
                       "Error processing upload. Confirm that the document uses the correct format.")
        return JsonResponse({'status': 'error', 'info': 'Error processing upload'})
    return JsonResponse({"status": "success", 'info': 'File uploaded successfully'})
