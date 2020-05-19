from django.core.management.base import BaseCommand
import os

from careweb.settings import BASE_DIR
from client.models import UploadedClient
import pyexcel as excel


class Command(BaseCommand):

    def handle(self, *args, **options):
        records = excel.iget_records(file_name=os.path.join(BASE_DIR, "otherstatic/enrollee.xlsx"))
        """
        first_name	middle_name	last_name	salutation	gender	phone_number	date_of_birth	age_today	
        marital_status	sub_region	participant_status	date_created	policy_status	policy_activation_date	
        policy_expiry_date	relationship	membership_number	policy_number	insurance_package	premium_amount	
        participant_policy_status	provider_code	provider_name	provider_ownership	state_id	national_id	passport
        staff_id	driving_licence	voter_id	military_id	secondary_phone_number	employer	agent	
        agent_phone_number	registration_agency	administration_agency
        """

        columns = ["first_name", "middle_name", "last_name", "salutation", "gender", "phone_number", "date_of_birth",
                   "age_today", "marital_status", "sub_region", "participant_status", "date_created", "policy_status",
                   "policy_activation_date", "policy_expiry_date", "relationship", "membership_number", "policy_number",
                   "insurance_package", "premium_amount", "participant_policy_status", "provider_code", "provider_name",
                   "provider_ownership", "state_id", "national_id", "passport", "staff_id", "driving_licence",
                   "voter_id", "military_id", "secondary_phone_number", "employer", "agent", "agent_phone_number",
                   "registration_agency", "administration_agency"]

        UploadedClient.objects.all().delete()
        print(UploadedClient.objects.count())
        for record in records:
            row = {key: record.get(key) if record.get(key) else "" for key in columns}
            uc = UploadedClient(**row)
            if uc.phone_number:
                uc.save()
        print(UploadedClient.objects.count(), " clients uploaded")
