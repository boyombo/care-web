from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from location.serializers import LGASerializer
from provider.models import CareProvider


class ProviderSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(source_field="provider.CareProvider.id", read_only=True)
    lga_id = PrimaryKeyRelatedField(pk_field=HashidSerializerCharField(source_field="location.LGA.id"), read_only=True)
    # lga = LGASerializer()

    class Meta:
        model = CareProvider
        fields = ['id', 'code_no', 'name', 'address', 'phone1', 'phone2', 'lga_id']
