from rest_framework import serializers

from core.models import Plan, PlanRate


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['name', 'code', 'id', 'size', 'has_extra', 'family_inclusive']


class PlanRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanRate
        fields = ['plan_id', 'id', 'payment_cycle', 'rate', 'extra_rate']
