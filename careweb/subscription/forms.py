from django import forms

from subscription.models import SubscriptionPayment

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit, Row, Column


class SubscriptionForm(forms.ModelForm):
    payment_date = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={"style": "display: inline-block; width: 33%;"}, years=[2018, 2019]
        )
    )

    class Meta:
        model = SubscriptionPayment
        fields = ["payment_date", "payment_type", "amount", "bank", "name"]
