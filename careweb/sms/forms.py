from django import forms

from sms.models import SmsLog


class SmsLogAdminForm(forms.ModelForm):
    class Meta:
        model = SmsLog
        fields = ['category', 'plan', 'recipients', 'message']
