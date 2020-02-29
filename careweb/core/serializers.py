from rest_framework import serializers

from core.models import Plan, PlanRate


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['name', 'code', 'id', 'size']


class PlanRateSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = PlanRate
        fields = ['plan', 'payment_cycle', 'rate', 'extra_rate']
