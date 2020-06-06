from django.contrib import admin, messages

from sms.forms import SmsLogAdminForm
from sms.models import SmsLog


class SmsLogAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'js/sms_admin.js',
        )

    list_display = ('category', 'plan_name', 'created', 'sender_name', 'status')
    list_filter = ('category', 'status')
    date_hierarchy = 'created'
    form = SmsLogAdminForm

    def save_model(self, request, obj, form, change):
        if obj.pk:
            messages.warning(request, "Action completed successfully. No change was applied!")
            return
        else:
            category = obj.category
            if category == "A":
                pass
            obj.sender = request.user
            super(SmsLogAdmin, self).save_model(request, obj, form, change)


admin.site.register(SmsLog, SmsLogAdmin)
