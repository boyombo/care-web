from django import forms
from django.contrib import messages

from provider.models import CareProvider, ProviderComment
from provider.util import is_valid_provider_mail


class CareProviderFormAdmin(forms.ModelForm):
    class Meta:
        model = CareProvider
        fields = ['email', 'code_no', 'name', 'address', 'phone1', 'phone2', 'lga']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not is_valid_provider_mail(self.instance.id, email):
            messages.error(self.http_request, "Email already in use")
            raise forms.ValidationError("Email already in use", code="email")
        return email


class ProviderCommentForm(forms.ModelForm):
    class Meta:
        model = ProviderComment
        fields = ['doctor', 'comment']
        widgets = {
            'doctor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Doctor's name"}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'})
        }
