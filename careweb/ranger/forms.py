from django import forms
from django.contrib.auth.models import User
import ranger.models as rm


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


class RangerForm(forms.ModelForm):

    class Meta:
        model = rm.Ranger
        fields = '__all__'


class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', )

    username.widget.attrs.update({'class': 'input100"', 
                               'placeholder': 'username'})
    password.widget.attrs.update({'class': 'input100"',
                                  'placeholder': 'password'})