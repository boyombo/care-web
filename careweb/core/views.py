from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.views.generic import TemplateView

from ratelimit.decorators import ratelimit

from client.utils import get_username_for_auth
from core.forms import (
    LoginForm,
    ForgotPwdForm,
    ChangePwdForm,
    ChangePwdForm2,
    ResetPasswordForm,
)
from core.models import Plan
from core.utils import send_reset_mail
from ranger.models import Ranger
from client.models import Client
from provider.models import CareProvider
from location.models import LGA

import django_excel as excel

import logging

logger = logging.getLogger(__name__)


class PostRegisterView(TemplateView):
    template_name = "post_register.html"

    def get(self, request, *args, **kwargs):
        if "/client/register/" in request.META.get("HTTP_REFERER", "/"):
            return super().get(request, *args, **kwargs)
        else:
            return redirect("register")


@csrf_exempt
def login_agent(request):
    logger.info("logging in agent")
    if request.method == "POST":
        form = LoginForm(request.POST)
        logger.info("form is {}".format(form))
        if form.is_valid():
            logger.info("form is valid")
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            usr = authenticate(username=username, password=password)
            if usr is not None:
                logger.info("authenticated {}".format(username))

                try:
                    agent = Ranger.objects.get(user=usr)
                except Ranger.DoesNotExist:
                    return JsonResponse(
                        {"error": "The user is not a ranger", "success": False}
                    )
                else:
                    logger.info("everything seems fine")
                    providers = [
                        {
                            "id": prov.id.hashid,
                            "name": prov.name,
                            "address": prov.address,
                            "phone1": prov.phone1,
                            "phone2": prov.phone2,
                            "lga_name": prov.lga.name,
                            "lga_id": prov.lga.id.hashid,
                        }
                        for prov in CareProvider.objects.all()
                    ]
                    logger.info("PROVIDERS")
                    logger.info(providers)

                    lgas = [
                        {"id": lga.id.hashid, "name": lga.name}
                        for lga in LGA.objects.all()
                    ]
                    logger.info("LGAS")
                    logger.info(lgas)

                    out = {
                        "success": True,
                        "ranger": {
                            "id": agent.id.id,
                            "username": agent.user.username,
                            "first_name": agent.first_name,
                            "last_name": agent.last_name,
                            "phone": agent.phone,
                            "lga_name": agent.lga.name,
                            "lga_id": agent.lga.id.hashid,
                            "balance": "{}".format(agent.balance),
                        },
                        "providers": providers,
                        "lgas": lgas,
                    }
                    # import pdb;pdb.set_trace()
                    return JsonResponse(out)
        return JsonResponse({"error": "Wrong credentials", "success": False})
    return JsonResponse({"error": "Bad Request", "success": False})


@ratelimit(key="ip", rate="10/h", block=True)
@csrf_exempt
def forgot(request):
    if request.method == "POST":
        from_app = True if request.GET.get("app") == "1" else False
        form = ForgotPwdForm(request.POST)
        if form.is_valid():
            # send email
            usr = form.cleaned_data["email"]
            # build reset confirmation url
            _id = None
            name = ""
            # try:
            #    ranger = Ranger.objects.get(user=usr)
            # except Ranger.DoesNotExist:
            try:
                clt = Client.objects.get(user=usr)
            except Client.DoesNotExist:
                pass
            else:
                _id = clt.id.hashid
                name = clt.first_name

            if not _id:
                try:
                    rng = Ranger.objects.get(user=usr)
                except Ranger.DoesNotExist:
                    pass
                else:
                    _id = rng.id.hashid
                    name = rng.first_name

            if _id:
                token = default_token_generator.make_token(usr)
                host = request.get_host()
                _url = reverse("password_reset_confirm", args=[_id, token])
                reset_link = "https://{}{}".format(host, _url)
                send_reset_mail(usr.username, name, reset_link)

            if from_app:
                return JsonResponse({"success": True})
            else:
                return redirect("password_reset_done")
        else:
            errors = form.errors
            if from_app:
                return JsonResponse({"success": False, "errors": errors})
            # else:
            #    return redirect("password_reset_done")
    else:
        form = ForgotPwdForm()
    return render(request, "registration/password_reset_form.html", {"form": form})


def reset_confirm(request, uid, token):
    # import pdb; pdb.set_trace()
    usr = None
    # try:
    #    ranger = Ranger.objects.get(pk=uid)
    # except Ranger.DoesNotExist:
    try:
        clt = Client.objects.get(pk=uid)
    except Client.DoesNotExist:
        pass
        # return HttpResponseBadRequest("Invalid request")
    else:
        usr = clt.user

    if not usr:
        try:
            rng = Ranger.objects.get(pk=uid)
        except Ranger.DoesNotExist:
            pass
        else:
            usr = rng.user
    if not usr:
        return HttpResponseBadRequest("Invalid Request")
    # else:
    #    usr = ranger.user
    # check if token is valid
    is_valid_token = default_token_generator.check_token(usr, token)
    if not is_valid_token:
        return HttpResponseBadRequest("Invalid request")

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data["new_password1"]
            usr.set_password(pwd)
            usr.save()
            return redirect("password_reset_complete")
    else:
        form = ResetPasswordForm()
    return render(request, "registration/password_reset_confirm.html", {"form": form})


@csrf_exempt
def change_pwd(request):
    if request.method == "POST":
        form = ChangePwdForm(request.POST)
        if form.is_valid():
            # import pdb;pdb.set_trace()
            username = form.cleaned_data["username"]
            pwd = form.cleaned_data["new_password"]
            un = get_username_for_auth(username)  # Enables authentication with phone no
            usr = User.objects.get(username=un)
            usr.set_password(pwd)
            usr.is_active = True
            usr.save()
            client = Client.objects.get(user=usr)
            client.uses_default_password = False
            client.verified = True
            client.save()
            return JsonResponse({"success": True})
    return JsonResponse({"success": False})


def change_pwd_web(request):
    usr = request.user
    clt = get_object_or_404(Client, user=usr)
    if request.method == "POST":
        # import pdb; pdb.set_trace()
        form = ChangePwdForm2(request.POST, usr=usr)
        if form.is_valid():
            pwd = form.cleaned_data["new_password"]
            usr.set_password(pwd)
            usr.save()
            return redirect("profile")
    else:
        form = ChangePwdForm2(usr=usr)
    return render(request, "client/change_password.html", {"form": form, "object": clt})


@login_required
def admin_reports(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('login'))
    date_range = request.GET.get('range')
    start_date = None
    end_date = None
    start = ""
    end = ""
    if date_range:
        try:
            date_range = str(date_range).split('-')
            start = date_range[0].strip()
            end = date_range[1].strip()
            start_date = datetime.strptime(start, "%m/%d/%Y").date()
            end_date = datetime.strptime(end, "%m/%d/%Y").date()
        except Exception as e:
            messages.error(request, "Invalid date range")
            print(e)
            return HttpResponseRedirect(reverse('admin_reports'))
    rangers = Ranger.objects.count()
    clients = Client.objects.all()
    if start_date and end_date:
        rangers = Ranger.objects.filter(created__date__gte=start_date, created__date__lte=end_date).count()
        clients = clients.filter(registration_date__date__gte=start_date, registration_date__date__lte=end_date)
    plans = Plan.objects.all()
    output = [
        {
            "title": "Rangers",
            "count": rangers
        }
    ]
    for plan in plans:
        title = "Enrollees on %s package" % plan.name
        output.append({
            "title": title,
            "count": clients.filter(plan=plan).count()
        })
    return render(request, "core/admin_report.html", {"reports": output, "start": start, "end": end})


@login_required
def export_admin_report(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('login'))
    if not request.method == 'POST':
        messages.error(request, "Invalid request")
        return HttpResponseRedirect(reverse('admin_reports'))
    start = request.POST.get('start')
    end = request.POST.get('end')
    start_date = None
    end_date = None
    if start and end:
        try:
            start_date = datetime.strptime(start, "%m/%d/%Y").date()
            end_date = datetime.strptime(end, "%m/%d/%Y").date()
        except:
            messages.error(request, "Invalid date range")
            return HttpResponseRedirect(reverse('admin_reports'))
    rangers = Ranger.objects.count()
    clients = Client.objects.all()
    if start_date and end_date:
        rangers = Ranger.objects.filter(created__date__gte=start_date, created__date__lte=end_date).count()
        clients = clients.filter(registration_date__date__gte=start_date, registration_date__date__lte=end_date)
    plans = Plan.objects.all()
    column_names = [
        "S/N", "Title", "Total %s" % ("({0} - {1})".format(start, end) if start and end else "")
    ]
    output = [
        column_names,
        [1, "Rangers", rangers]
    ]
    count = 2
    for plan in plans:
        title = "Enrollees on %s package" % plan.name
        output.append([count, title, clients.filter(plan=plan).count()])
        count += 1
    sheet = excel.pe.Sheet(output)
    return excel.make_response(sheet, "xls", file_name="Futurecare monthly report")


@login_required
def admin_landing_page(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'core/admin_landing.html')
