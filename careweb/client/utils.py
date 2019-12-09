from subscription.utils import get_subscription_rate
from client.models import Dependant, ClientAssociation


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
    dependants = [
        {
            "dob": dependant.dob.strftime("%Y-%m-%d"),
            "first_name": dependant.first_name,
            "surname": dependant.surname,
            "middle_name": dependant.middle_name,
            "relationship": dependant.relationship,
            "pcp": dependant.pcp.id.id if dependant.pcp else None,
        }
        for dependant in Dependant.objects.filter(primary=client)
    ]
    associations = [
        assoc.association.id.id
        for assoc in ClientAssociation.objects.filter(client=client)
    ]
    return {
        "active": client.verified,
        "subscription_rate": subscription_rate,
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
        "lashmaNo": client.lashma_no,
        "lashmaQualityLifeNo": client.lashma_quality_life_no,
        "pcp": client.pcp.id.id if client.pcp else None,
        "ranger": client.ranger.id.id if client.ranger else None,
        "homeAddress": client.home_address,
        "occupation": client.occupation,
        "company": client.company,
        "officeAddress": client.office_address,
        "packageOption": client.package_option,
        "plan": client.plan.id if client.plan else None,
        "paymentOption": client.payment_option,
        "paymentInstrument": client.payment_instrument,
        "dependants": dependants,
        "associations": associations,
    }
