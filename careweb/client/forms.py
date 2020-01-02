from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.functional import lazy
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from client.models import Client, Association, Dependant
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from provider.models import CareProvider
from location.models import LGA


class ApiRegForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ["email", "first_name", "surname"]

    def clean_email(self):
        if "email" in self.cleaned_data:
            email = self.cleaned_data["email"]
            try:
                User.objects.get(username=email)
            except User.DoesNotExist:
                return email
            else:
                raise forms.ValidationError("The email has already been used")


class RegForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ["email", "first_name", "surname"]

    def clean_email(self):
        if "email" in self.cleaned_data:
            email = self.cleaned_data["email"]
            try:
                User.objects.get(username=email)
            except User.DoesNotExist:
                return email
            else:
                raise forms.ValidationError("The email has already been used")

    def clean(self):
        if "password" in self.cleaned_data and "confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["confirm"]:
                raise forms.ValidationError("The passwords do not match!")
            return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean(self):
        if "username" in self.cleaned_data and "password" in self.cleaned_data:
            username = self.cleaned_data["username"]
            password = self.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Wrong username/password")
            # try:
            #    Client.objects.get(user=user)
            # except Client.DoesNotExist:
            #    raise forms.ValidationError(
            #        "Your account is not registered as a client"
            #    )
            return self.cleaned_data


class PersonalInfoForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={"style": "display: inline-block; width: 33%;"},
            years=range(1950, timezone.now().year),
        )
    )

    class Meta:
        model = Client
        fields = [
            "first_name",
            "surname",
            "middle_name",
            "dob",
            "sex",
            "marital_status",
        ]

    def clean_dob(self):
        if "dob" in self.cleaned_data:
            dob = self.cleaned_data["dob"]
            eighteen = timezone.now().date() - relativedelta(years=18)
            if dob > eighteen:
                raise forms.ValidationError("You must be at least 18 years old")
        return self.cleaned_data["dob"]


def get_association_choices():
    return [(i.id, i.name) for i in Association.objects.all()]


class AssociationsForm(forms.Form):
    associations = forms.MultipleChoiceField(
        choices=get_association_choices, widget=forms.CheckboxSelectMultiple(),
    )


class DependantForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={"style": "display: inline-block; width: 33%;"},
            years=range(1970, 2019),
        )
    )
    # lga = forms.ModelChoiceField(queryset=LGA.objects.all(), required=False)

    class Meta:
        model = Dependant
        exclude = ["primary"]

    def __init__(self, *args, **kwargs):
        self.primary = kwargs.pop("primary")
        super().__init__(*args, **kwargs)

    def clean_relationship(self):
        if "relationship" in self.cleaned_data:
            if (
                Dependant.objects.filter(
                    primary=self.primary, relationship=Dependant.SPOUSE
                )
                and self.cleaned_data["relationship"] == Dependant.SPOUSE
            ):
                raise forms.ValidationError("You can have only one spouse on the plan")
        return self.cleaned_data["relationship"]

        # self.fields["pcp"].queryset = CareProvider.objects.none()

        # if "lga" in self.data:
        #    try:
        #        lga_id = self.data.get("lga")
        #        self.fields["pcp"].queryset = CareProvider.objects.filter(
        #            lga__id=lga_id
        #        )
        #    except (TypeError, ValueError):
        #        pass
        # elif self.instance.pk:
        #    self.fields["pcp"].queryset = CareProvider.objects.all()


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["photo"]


class AmountForm(forms.Form):
    amount = forms.FloatField()


class PlanForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["plan", "payment_option", "payment_instrument"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("payment_date_month", css_class="form-group col-md-4 mb-0"),
                Column("payment_date_day", css_class="form-group col-md-4 mb-0"),
                Column("payment_date_year", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
        )


class PCPForm(forms.ModelForm):
    lga = forms.ModelChoiceField(queryset=LGA.objects.all())

    class Meta:
        model = Client
        fields = ["pcp"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pcp"].queryset = CareProvider.objects.none()
        # import pdb;pdb.set_trace()

        if "lga" in self.data:
            try:
                lga_id = self.data.get("lga")
                self.fields["pcp"].queryset = CareProvider.objects.filter(
                    lga__id=lga_id
                )
            except (TypeError, ValueError):
                pass
        elif self.instance.pk:
            self.fields["pcp"].queryset = CareProvider.objects.all()


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = [
            "balance",
            "verification_code",
            "photo",
            "registration_date",
            "package_option",
            "hmo",
        ]
