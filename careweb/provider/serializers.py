from hashid_field.rest import HashidSerializerCharField, HashidSerializerIntegerField
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from location.serializers import LGASerializer
from provider.models import CareProvider


class ProviderSerializer(serializers.ModelSerializer):
    id = HashidSerializerIntegerField(source_field="provider.CareProvider.id", read_only=True)
    pk = HashidSerializerCharField(source_field="provider.CareProvider.id", read_only=True)
    lga_id = PrimaryKeyRelatedField(pk_field=HashidSerializerIntegerField(source_field="location.LGA.id"), read_only=True)
    lga = LGASerializer()

    class Meta:
        model = CareProvider
        fields = ['id', 'code_no', 'name', 'address', 'phone1', 'phone2', 'lga_id', 'lga', 'pk']
