from rest_framework import serializers

from subscription.models import SubscriptionPayment


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    ranger_id = serializers.CharField(max_length=120, required=False)
    client_id = serializers.CharField(max_length=120, required=False)

    class Meta:
        model = SubscriptionPayment
        fields = ['client_id', 'amount', 'bank', 'name', 'payment_type', 'ranger_id']


class SubscriptionPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPayment
        fields = "__all__"
