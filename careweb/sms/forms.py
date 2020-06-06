from django import forms

from sms.models import SmsLog


class SmsLogAdminForm(forms.ModelForm):
    class Meta:
        model = SmsLog
        fields = ['sms_sender', 'category', 'plan', 'recipients', 'message']
