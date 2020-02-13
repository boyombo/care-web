from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.functional import lazy
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.password_validation import validate_password

from client.models import Client, Association, Dependant
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from provider.models import CareProvider
from location.models import LGA


class BasicRegForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["first_name", "surname", "phone_no"]


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
    password = forms.CharField(
        max_length=100, widget=forms.PasswordInput, validators=[validate_password]
    )
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

    # def clean_password(self):
    #    if "password" in self.cleaned_data:
    #        validated = validate_password(self.cleaned_data["password"])


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean(self):
        if "username" in self.cleaned_data and "password" in self.cleaned_data:
            username = self.cleaned_data["username"]
            password = self.cleaned_data["password"]
            if not username.__contains__("@"):
                # this is probably a phone number
                if Client.objects.filter(phone_no=username).exists():
                    client = Client.objects.get(phone_no=username)
                    email = client.email
                else:
                    # User typed an invalid string
                    email = ""
            else:
                email = username
            user = authenticate(username=email, password=password)
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


class ClientAdminForm(forms.ModelForm):
    lga = forms.ModelChoiceField(queryset=LGA.objects.all(), required=False)

    class Meta:
        model = Client
        widgets = {
            "pcp": forms.Select(attrs={"class": "form-control select2", "style": "min-width: 250px"})
        }
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pcp"].queryset = CareProvider.objects.none()

        if "lga" in self.data:
            try:
                lga_id = self.data.get("lga")
                self.fields["pcp"].queryset = CareProvider.objects.filter(lga__id=lga_id)
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


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "New Password"}))
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Retype Password"}))

    def clean_confirm_password(self):
        password = self.cleaned_data.get('new_password')
        confirm = self.cleaned_data.get('confirm_password')
        if confirm != password:
            raise forms.ValidationError("Password fields must match", code="confirm_password")
        return confirm
