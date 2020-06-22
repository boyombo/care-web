from django.contrib import admin
from django.contrib.auth.models import User, Permission
from simple_history.admin import SimpleHistoryAdmin
from constance import config

from careweb.utils import HashIdFieldAdminMixin
from core.utils import send_email
from provider.forms import CareProviderFormAdmin
from provider.models import CareProvider
from provider.util import is_valid_provider_mail


@admin.register(CareProvider)
class CareProviderAdmin(HashIdFieldAdminMixin, SimpleHistoryAdmin):
    list_display = ['name', 'phone1', 'lga']
    list_filter = ['lga']
    search_fields = ['name']
    form = CareProviderFormAdmin

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(CareProviderAdmin, self).get_form(request, obj, change, **kwargs)
        form.http_request = request
        return form

    def save_model(self, request, obj, form, change):
        email = obj.email
        if email and is_valid_provider_mail(obj.id, email):
            if not User.objects.filter(username=email).exists():
                # print("Provider does not currently have a user attached")
                password = config.CLIENT_DEFAULT_PASSWORD
                user = User.objects.create_user(email, email=email, password=password, first_name=obj.name)
                user.user_permissions.add(Permission.objects.get(codename='is_provider'))
                user.save()
                obj.uses_default_password = True
                try:
                    context = {"name": obj.name, "username": email, "password": password}
                    send_email(obj.email, "provider_welcome_email", context)
                except:
                    pass
                # print("User created for the client")
        super(CareProviderAdmin, self).save_model(request, obj, form, change)
