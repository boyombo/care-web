from django import forms
from django.contrib.auth.models import User

import client.models as cm


class DateInput(forms.DateInput):
    input_type = 'date'


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    pwd1 = forms.CharField(widget=forms.PasswordInput())
    pwd2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = cm.Client
        fields = [
            'middle_name',
            'dob', 'sex', 'marital_status', 'phone_no', 'whatsapp_no']
            # 'surname', 'first_name', 

        widgets = {'dob': DateInput()}

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


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password', )

    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput)
    

    email.widget.attrs.update({'class': 'form-control',
                               'placeholder': 'Email'})
    password.widget.attrs.update({'class': 'form-control',
                               'placeholder': 'password'})
    password2.widget.attrs.update({'class': 'form-control',
                               'placeholder': 'Confirm password'})
    username.widget.attrs.update({'class': 'input--style-1', 
                               'placeholder': 'username'})


class ClientForm(forms.ModelForm):

    class Meta:
        model = cm.Client
        fields = '__all__'


class InsuranceForm(forms.ModelForm):

    class Meta:
        model = cm.Insurance
        fields = '__all__'
