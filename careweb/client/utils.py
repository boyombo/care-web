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
    }


def get_verification_code():
    code = ""
    for i in range(config.LEN_VERIFICATION_CODE):
        code += choice(digits)
    if Client.objects.filter(verification_code=code).exists():
        return get_verification_code()
    return code
