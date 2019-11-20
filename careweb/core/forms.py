from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class ForgotPwdForm(forms.Form):
    email = forms.CharField(max_length=100)

    def clean_email(self):
        if "email" in self.cleaned_data:
            try:
                User.objects.get(username=self.cleaned_data["email"])
            except User.DoesNotExist:
                raise forms.ValidationError("No user exists with this email")
            else:
                return self.cleaned_data["email"]


class ChangePwdForm(forms.Form):
    email = forms.CharField(max_length=100)
    old_password = forms.CharField(max_length=100)
    new_password = forms.CharField(max_length=100)

    def clean(self):
        if "email" in self.cleaned_data and "old_password" in self.cleaned_data:
            email = self.cleaned_data["email"]
            pwd = self.cleaned_data["old_password"]
            usr = authenticate(username=email, password=pwd)
            if not usr:
                raise forms.ValidationError("Username or password invalid")
            return self.cleaned_data
