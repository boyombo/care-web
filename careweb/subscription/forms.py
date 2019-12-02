from django import forms

from subscription.models import SubscriptionPayment


class SubscriptionForm(forms.ModelForm):
    payment_date = forms.DateField(widget=forms.SelectDateWidget(years=[2018, 2019]))

    class Meta:
        model = SubscriptionPayment
        fields = ["payment_date", "payment_type", "amount", "bank", "name"]
