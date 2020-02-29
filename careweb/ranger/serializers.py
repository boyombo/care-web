from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from location.serializers import LGASerializer
from ranger.models import Ranger


class RangerSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(source_field="ranger.Ranger.id", read_only=True)
    lga = LGASerializer()

    class Meta:
        model = Ranger
        fields = ['id', 'username', 'phone', 'first_name', 'last_name', 'lga', 'balance']
