from django import forms

from client.models import Client


class RegForm(forms.ModelForm):
    password = forms.CharField(max_length=100)

    class Meta:
        model = Client
        fields = ['email', 'first_name', 'surname']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['photo']
