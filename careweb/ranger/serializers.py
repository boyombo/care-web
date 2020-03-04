from hashid_field.rest import HashidSerializerCharField, HashidSerializerIntegerField
from rest_framework import serializers

from location.serializers import LGASerializer
from payment.serializers import PaymentSerializer
from ranger.models import Ranger, WalletFunding


class RangerSerializer(serializers.ModelSerializer):
    id = HashidSerializerIntegerField(source_field="ranger.Ranger.id", read_only=True)
    pk = HashidSerializerCharField(source_field="ranger.Ranger.id", read_only=True)
    lga = LGASerializer()

    class Meta:
        model = Ranger
        fields = ['id', 'username', 'phone', 'first_name', 'last_name', 'lga', 'balance', 'pk']


class WalletFundingSerializer(serializers.ModelSerializer):
    id = HashidSerializerIntegerField(source_field="ranger.WalletFunding.id", read_only=True)
    ranger = RangerSerializer()
    payment = PaymentSerializer()

    class Meta:
        model = WalletFunding
        fields = "__all__"


class CreateFundingSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    bank = serializers.CharField(max_length=200)
    amount = serializers.DecimalField(decimal_places=2, max_digits=30)
    payment_date = serializers.DateField(input_formats=["%Y-%m-%d", ])
    payment_type = serializers.CharField(max_length=200)
    ranger_id = serializers.CharField(max_length=200)
