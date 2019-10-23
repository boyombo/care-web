from django import forms

from client.models import Client


class RegForm(forms.ModelForm):
    password = forms.CharField(max_length=100)

    class Meta:
        model = Client
        fields = ['email', 'first_name', 'surname', 'phone']
