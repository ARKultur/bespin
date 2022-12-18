from rest_framework import serializers

from api.serializers.utils import create_instance, create_mutiple_instances
from api.serializers import CustomerSerializer

from api.models.domains import Node, Address
from api.models import Customer

"""This modules stores the serializers related to administered domains"""


class NodeSerializer(serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Address.objects.all())

    class Meta:
        model = Node
        fields = ['latitude', 'longitude', 'name', 'id', 'address']


class AddressSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Customer.objects.all())

    class Meta:
        model = Address
        fields = [
            'country', 'country_code', 'postcode', 'state', 'state_district',
            'city', 'street', 'state_district', 'street_number', 'owner', 'id'
        ]

class NestedNodeSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False, read_only=False)

    class Meta:
        model = Node
        fields = '__all__'

    def create(self, validated_data):
        validated_data['address'] = create_instance(Address, validated_data, 'address')
        return Node.objects.get_or_create(**validated_data)

    def update(self, instance, validated_data):
        if 'address' in validated_data:
            nested_serializer = self.fields['address']
            nested_instance = instance.address
            nested_data = validated_data.pop('address')
            nested_serializer.update(nested_instance, nested_data)
        return super(NestedNodeSerializer, self).update(instance, validated_data)
