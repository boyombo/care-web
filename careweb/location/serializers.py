from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from location.models import LGA


class LGASerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(source_field="location.LGA.id", read_only=True)

    class Meta:
        model = LGA
        fields = ['id', 'name']
