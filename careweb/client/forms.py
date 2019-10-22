from django import forms
from django.contrib.auth.models import User

from client.models import Client


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    pwd1 = forms.CharField(widget=forms.PasswordInput())
    pwd2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Client
        fields = [
            'surname', 'first_name', 'middle_name',
            'dob', 'sex', 'marital_status', 'phone_no', 'whatsapp_no']

    widgets = {
        'dob': forms.DateInput(
            format=('%m/%d/%Y'),
            attrs={'class': 'form-control',
                   'placeholder': 'Date of Birth', 'type': 'date'}),
    }

    labels = {"sex": "Select Gender"}

    def clean_email(self):
        if 'username' in self.cleaned_data:
            username = self.cleaned_data['username']
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return username
            else:
                raise forms.ValidationError("Email already in use")

    def clean_pwd(self):
        if 'pwd1' in self.cleaned_data and 'pwd2' in self.cleaned_data:
            if self.cleaned_data['pwd1'] != self.cleaned_data['pwd2']:
                raise forms.ValidationError("The passwords does not match")
        return self.cleaned_data
