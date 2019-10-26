from django import forms
from django.contrib.auth import authenticate

from client.models import Client


class RegForm(forms.ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ['email', 'first_name', 'surname']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean(self):
        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Wrong username/password')
            try:
                Client.objects.get(user=user)
            except Client.DoesNotExist:
                raise forms.ValidationError(
                    'Your account is not registered as a client')
            return self.cleaned_data


class PersonalInfoForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1950, 2001)))

    class Meta:
        model = Client
        fields = ['first_name', 'surname', 'middle_name', 'dob',
                  'sex', 'marital_status']
