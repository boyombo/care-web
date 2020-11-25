from django import forms
from django.contrib.auth.models import User

from payment.models import Payment


class PaymentForm(forms.Form):
    email = forms.CharField(max_length=100)
    amount = forms.IntegerField()


class WalkinPaymentForm(forms.ModelForm):
    user = forms.CharField(max_length=200)

    class Meta:
        model = Payment
        fields = ["amount", "payment_date", "reference", "narration", "paid_by"]

    def clean_username(self):
        if "user" in self.cleaned_data:
            _username = self.cleaned_data["user"]
            try:
                User.objects.get(username=_username)
            except User.DoesNotExist:
                raise forms.ValidationError("User does not exist")
            else:
                return _username


class UssdPaymentForm(forms.ModelForm):
    phone = forms.CharField(max_length=20)

    class Meta:
        model = Payment
        fields = ["amount", "payment_date", "reference", "narration", "paid_by", "phone"]
