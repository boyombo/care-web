from django.contrib import admin, messages

from sms.forms import SmsLogAdminForm
from sms.models import SmsLog
from sms.utils import get_client_contacts, send_multi_sms


class SmsLogAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'js/sms_admin.js',
        )

    list_display = ('category', 'plan_name', 'created', 'sms_sender', 'status')
    list_filter = ('category', 'status')
    date_hierarchy = 'created'
    form = SmsLogAdminForm

    def save_model(self, request, obj, form, change):
        if obj.pk:
            messages.warning(request, "Action completed successfully. No change was applied!")
            return
        else:
            category = obj.category
            contacts = get_client_contacts(category, obj.plan, obj.recipients)
            # print(contacts)
            status = send_multi_sms(contacts, obj.message, obj.sms_sender)
            obj.created_by = request.user
            if obj.recipients:
                obj.recipients = ",".join(contacts)
            obj.status = "S" if str(status) == "200" else "F"
            super(SmsLogAdmin, self).save_model(request, obj, form, change)


admin.site.register(SmsLog, SmsLogAdmin)
