from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from client.utils import get_username_for_auth


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class ForgotPwdForm(forms.Form):
    email = forms.CharField(max_length=100)

    def clean_email(self):
        if "email" in self.cleaned_data:
            try:
                user = User.objects.get(username=self.cleaned_data["email"])
            except User.DoesNotExist:
                raise forms.ValidationError("No user exists with this email")
            else:
                return user


class ChangePwdForm(forms.Form):
    username = forms.CharField(max_length=100)
    old_password = forms.CharField(max_length=100)
    new_password = forms.CharField(max_length=100)

    def clean(self):
        if "username" in self.cleaned_data and "old_password" in self.cleaned_data:
            username = self.cleaned_data["username"]
            pwd = self.cleaned_data["old_password"]
            un = get_username_for_auth(username)  # Enables authentication with phone no
            usr = authenticate(username=un, password=pwd)
            if not usr:
                raise forms.ValidationError("Username or password invalid")
            return self.cleaned_data


class ChangePwdForm2(forms.Form):
    # email = forms.CharField(max_length=100, widget=forms.HiddenInput)
    current_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("usr")
        super().__init__(*args, **kwargs)

    def clean(self):
        if (
            "current_password" in self.cleaned_data
            and "new_password" in self.cleaned_data
            and "confirm_new_password" in self.cleaned_data
        ):
            # import pdb; pdb.set_trace()
            pwd1 = self.cleaned_data["new_password"]
            pwd2 = self.cleaned_data["confirm_new_password"]
            if pwd1 != pwd2:
                raise forms.ValidationError("Passwords do not match")
            pwd = self.cleaned_data["current_password"]
            email = self.user.username
            usr = authenticate(username=email, password=pwd)
            if not usr:
                raise forms.ValidationError("Password is not correct")
            return self.cleaned_data


class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput)
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean_new_password2(self):
        pass1 = self.cleaned_data.get('new_password1')
        pass2 = self.cleaned_data.get('new_password2')
        if pass2 != pass1:
            raise forms.ValidationError("Password fields must match", code="new_password2")
        return pass2
