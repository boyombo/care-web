from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField, HashidSerializerIntegerField
from rest_framework.relations import PrimaryKeyRelatedField

from client.models import Dependant, Client, HMO, Association, ClientAssociation
from core.serializers import PlanSerializer
from location.serializers import LGASerializer
from provider.serializers import ProviderSerializer
from ranger.serializers import RangerSerializer


class AssociationSerializer(serializers.ModelSerializer):
    id = HashidSerializerIntegerField(source_field="client.Association.id", read_only=True)

    class Meta:
        model = Association
        fields = ['id', 'name']


class ClientAssociationSerializer(serializers.ModelSerializer):
    id = HashidSerializerIntegerField(source_field="client.ClientAssociation.id", read_only=True)
    client_id = PrimaryKeyRelatedField(pk_field=HashidSerializerIntegerField(source_field="client.Client.id"),
                                       read_only=True)
    association_id = PrimaryKeyRelatedField(pk_field=HashidSerializerIntegerField(source_field="client.Association.id"),
                                            read_only=True)

    class Meta:
        model = ClientAssociation
        fields = ['id', 'client_id', 'association_id', 'association_name']


class HMOSerializer(serializers.ModelSerializer):
    id = HashidSerializerIntegerField(source_field="client.HMO.id", read_only=True)

    class Meta:
        model = HMO
        fields = ['id', 'name', 'pk']


class DependantSerializer(serializers.ModelSerializer):
    primary_id = PrimaryKeyRelatedField(pk_field=HashidSerializerIntegerField(source_field="client.Client.id"),
                                        read_only=True)
    id = HashidSerializerIntegerField(source_field="client.Dependant.id", read_only=True)

    class Meta:
        model = Dependant
        fields = ['id', 'salutation', 'first_name', 'surname', 'middle_name', 'relationship', 'dob', 'primary_id']


class ClientSerializer(serializers.ModelSerializer):
    id = HashidSerializerIntegerField(source_field="client.Client.id", read_only=True)
    pk = HashidSerializerCharField(source_field="client.Client.id", read_only=True)
    pcp = ProviderSerializer()
    ranger = RangerSerializer()
    lga = LGASerializer()
    plan = PlanSerializer()
    hmo = HMOSerializer()
    associations = ClientAssociationSerializer(many=True)
    dependants = DependantSerializer(many=True)

    class Meta:
        model = Client
        fields = ['id', 'username', 'salutation', 'first_name', 'middle_name', 'surname', 'dob', 'sex',
                  'marital_status', 'national_id_card_no', 'drivers_licence_no', 'voters_card_no', 'whatsapp_no',
                  'international_passport_no', 'lashma_no', 'lashma_quality_life_no', 'lagos_resident_no', 'phone_no',
                  'email', 'pcp', 'ranger', 'lga', 'plan', 'payment_option', 'payment_instrument', 'hmo',
                  'formatted_dob',
                  'registration_date', 'photo_url', 'verification_code', 'balance', 'verified', 'subscription_rate',
                  'uses_default_password', 'company', 'home_address', 'occupation', 'office_address', 'imageUri',
                  'associations', 'pk', 'dependants']


class CreateDependantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependant
        fields = ['salutation', 'first_name', 'surname', 'middle_name', 'relationship', 'dob']


class CreateClientSerializer(serializers.ModelSerializer):
    id = HashidSerializerIntegerField(source_field="client.Client.id", read_only=True)
    dependents = CreateDependantSerializer(many=True, allow_null=True, required=False)
    hmo_id = serializers.CharField(max_length=120, allow_blank=True, required=False)
    pcp_id = serializers.IntegerField(required=False, allow_null=True)
    plan_id = serializers.IntegerField(required=False, allow_null=True)
    ranger_id = serializers.IntegerField()
    associations = serializers.ListField(child=serializers.IntegerField(min_value=1), allow_empty=True, allow_null=True,
                                         required=False)

    class Meta:
        model = Client
        fields = ['salutation', 'first_name', 'middle_name', 'surname', 'dob', 'sex', 'marital_status',
                  'national_id_card_no', 'drivers_licence_no', 'lashma_no', 'lashma_quality_life_no',
                  'lagos_resident_no', 'phone_no', 'whatsapp_no', 'email', 'company', 'home_address', 'occupation',
                  'office_address', 'international_passport_no', 'voters_card_no', 'payment_instrument',
                  'payment_option', 'hmo_id', 'pcp_id', 'plan_id', 'ranger_id', 'associations',
                  'dependents', 'id']


class UpdateClientSerializer(serializers.ModelSerializer):
    id = HashidSerializerIntegerField(source_field="client.Client.id", read_only=True)
    dependents = CreateDependantSerializer(many=True, allow_null=True, required=False)
    hmo_id = serializers.CharField(max_length=120, allow_blank=True, required=False)
    pcp_id = serializers.IntegerField(required=False, allow_null=True)
    plan_id = serializers.IntegerField(required=False, allow_null=True)
    associations = serializers.ListField(child=serializers.IntegerField(min_value=1), allow_empty=True, allow_null=True,
                                         required=False)

    class Meta:
        model = Client
        fields = ['salutation', 'first_name', 'middle_name', 'surname', 'dob', 'sex', 'marital_status',
                  'national_id_card_no', 'drivers_licence_no', 'lashma_no', 'associations',
                  'lagos_resident_no', 'phone_no', 'whatsapp_no', 'email', 'company', 'home_address', 'occupation',
                  'office_address', 'international_passport_no', 'voters_card_no', 'payment_instrument',
                  'payment_option', 'hmo_id', 'pcp_id', 'plan_id', 'dependents', 'id']
