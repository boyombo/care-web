from hashid_field.rest import HashidSerializerCharField, HashidSerializerIntegerField
from rest_framework import serializers

from location.models import LGA


class LGASerializer(serializers.ModelSerializer):
    id = HashidSerializerIntegerField(source_field="location.LGA.id", read_only=True)
    pk = HashidSerializerCharField(source_field="location.LGA.id", read_only=True)

    class Meta:
        model = LGA
        fields = ['id', 'name', 'pk']
