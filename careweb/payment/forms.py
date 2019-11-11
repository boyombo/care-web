from django import forms


class PaymentForm(forms.Form):
    email = forms.CharField(max_length=100)
    amount = forms.IntegerField()
