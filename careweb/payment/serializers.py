from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(source_field="payment.Payment.id", read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"
