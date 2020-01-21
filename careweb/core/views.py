from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.views.generic import TemplateView

from ratelimit.decorators import ratelimit

from core.forms import (
    LoginForm,
    ForgotPwdForm,
    ChangePwdForm,
    ChangePwdForm2,
    ResetPasswordForm,
)
from core.utils import send_reset_mail
from ranger.models import Ranger
from client.models import Client
from provider.models import CareProvider
from location.models import LGA

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


@ratelimit(key="ip", rate="3/h", block=True)
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
            # else:
            #    _id = ranger.id.hashid
            #    name = ranger.first_name

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
        return HttpResponseBadRequest("Invalid request")
    else:
        usr = clt.user
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
            username = form.cleaned_data["email"]
            pwd = form.cleaned_data["new_password"]
            usr = User.objects.get(username=username)
            usr.set_password(pwd)
            usr.save()
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
