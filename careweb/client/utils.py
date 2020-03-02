from random import choice
from string import digits

from subscription.utils import get_subscription_rate, get_next_subscription_date
from client.models import Dependant, ClientAssociation, Client
from django.utils import timezone
from constance import config


def get_quality_life_number(cl):
    yr = timezone.now().strftime("%y")
    # count = Client.objects.filter(registration_date__year=yr).count()
    return "QL{}{}".format(yr, str(cl.id.id + 1471).zfill(6))


def get_client_details(client, host):
    if client.photo:
        photo_url = "{}{}".format(host, client.photo.url)
    else:
        photo_url = ""
    if client.dob:
        dob = client.dob.strftime("%Y-%m-%d")
    else:
        dob = None
    subscription_rate = get_subscription_rate(client)
    next_subscription_date = get_next_subscription_date(client).strftime("%d %b %Y")
    dependants = [
        {
            "dob": dependant.dob.strftime("%Y-%m-%d"),
            "first_name": dependant.first_name,
            "surname": dependant.surname,
            "middle_name": dependant.middle_name,
            "relationship": dependant.relationship,
        }
        for dependant in Dependant.objects.filter(primary=client)
    ]
    associations = [
        assoc.association.id.id
        for assoc in ClientAssociation.objects.filter(client=client)
    ]
    if client.pcp:
        client_pcp = {
            "id": client.pcp.id.id,
            "name": client.pcp.name,
            "lga_id": client.pcp.lga.id.id,
            "address": client.pcp.address,
            "phone1": client.pcp.phone1,
        }
    else:
        client_pcp = None
    return {
        "active": client.verified,
        "subscription_rate": subscription_rate,
        "next_subscription_date": next_subscription_date,
        "id": client.id.id,
        "surname": client.surname,
        "firstName": client.first_name,
        "phone": client.phone_no,
        "whatsapp": client.whatsapp_no,
        "email": client.email,
        "imageUri": photo_url,
        "dob": dob,
        "sex": client.sex,
        "maritalStatus": client.marital_status,
        "nationalIdNo": client.national_id_card_no,
        "driversLicenceNo": client.drivers_licence_no,
        "lagosResidentsNo": client.lagos_resident_no,
        "votersCardNo": client.voters_card_no,
        "internationalPassportNo": client.international_passport_no,
        "lashmaNo": client.lashma_no,
        "lashmaQualityLifeNo": client.lashma_quality_life_no,
        "verification_code": client.verification_code,
        "pcp": client_pcp,
        "ranger": client.ranger.id.id if client.ranger else None,
        "homeAddress": client.home_address,
        "occupation": client.occupation,
        "company": client.company,
        "officeAddress": client.office_address,
        "packageOption": client.package_option,
        "plan": client.plan.id if client.plan else None,
        "paymentOption": client.payment_option,
        "paymentInstrument": client.payment_instrument,
        "dependents": dependants,  # I call it dependents instead of dependants everywhere
        "associations": associations,
        "usesDefaultPassword": client.uses_default_password
    }


def get_verification_code():
    code = ""
    for i in range(config.LEN_VERIFICATION_CODE):
        code += choice(digits)
    if Client.objects.filter(verification_code=code).exists():
        return get_verification_code()
    return code


def get_username_for_auth(username_input):
    # Clients may want to sign in with phone no
    username = username_input
    if not username_input.__contains__("@"):
        # this is probably a phone number
        if Client.objects.filter(phone_no=username_input).exists():
            client = Client.objects.get(phone_no=username_input)
            username = client.user.username
    else:
        if Client.objects.filter(email=username_input).exists():
            client = Client.objects.get(email=username_input)
            username = client.user.username
    return username


def phone_no_valid(phone_no, client_id):
    if not phone_no:
        return True
    if not Client.objects.filter(phone_no=phone_no).exists():
        return True
    client = Client.objects.get(phone_no=phone_no)
    return str(client.id) == client_id


def email_valid(email, client_id):
    if not email:
        return True
    if not Client.objects.filter(email__iexact=email).exists():
        return True
    client = Client.objects.get(email=email)
    return str(client.id) == client_id


def is_registered_user(client_id):
    if not client_id:
        return False
    if not Client.objects.filter(id=str(client_id)).exists():
        return False
    client = Client.objects.get(id=str(client_id))
    return client.user is not None


def get_export_row(client, index):
    rows = []
    ind = index
    i = str(ind)
    sub = client.subscription_rate if client.subscription_rate and client.subscription_rate != "None" else ""
    lga = str(client.lga) if client.lga else ""
    plan = str(client.plan) if client.plan else ""
    date = client.dob.strftime("%B %d, %Y") if client.dob else ""
    rows.append([i, client.get_salutation, client.first_name, client.middle_name, client.surname,
                 date, client.phone_no, "Principal", client.sex, sub,
                 client.lagos_resident_no, client.national_id_card_no, client.international_passport_no, "",
                 client.voters_card_no, client.drivers_licence_no, "", lga, client.provider_name,
                 plan, client.payment_option, "", ""])
    relationships = ["Spouse", "Daughter", "Son", "Others"]
    for dependent in Dependant.objects.filter(primary=client):
        ind += 1
        i = str(ind)
        date = dependent.dob.strftime("%B %d, %Y") if dependent.dob else ""
        rel = relationships[dependent.relationship] if dependent.relationship else ''
        rows.append([i, dependent.get_salutation, dependent.first_name, dependent.middle_name, dependent.surname,
                     date, "", rel, dependent.sex, "", "", "", "", "", "", "", "", "", "",
                     "", "", "", ""])
    return rows
