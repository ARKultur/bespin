from rest_framework import serializers

from api.serializers.utils import create_instance, create_mutiple_instances
from api.serializers import CustomerSerializer

from api.models.domains import Node, Address
from api.models import Customer

"""This modules stores the serializers related to administered domains"""


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['latitude', 'longitude', 'name']


class NestedAddressSerializer(serializers.ModelSerializer):
    owner = CustomerSerializer(many=False, read_only=False)
    nodes = NodeSerializer(source='node_set', many=True, read_only=True)

    class Meta:
        model = Address
        fields = [
            'nodes', 'owner', 'country', 'country_code', 'postcode',
            'state', 'state_district', 'city', 'street', 'state_district'
        ]

    def create(self, validated_data):
        validated_data['owner'] = create_instance(Customer, validated_data, 'owner')
        return Address.objects.get_or_create(**validated_data)


    def update(self, instance, validated_data):
        if 'owner' in validated_data:
            nested_serializer = self.fields['owner']
            nested_instance = instance.owner
            nested_data = validated_data.pop('owner')
            nested_serializer.update(nested_instance, nested_data)

        if 'nodes' in validated_data:
            nested_serializer = self.fields['nodes']
            nested_instance = instance.nodes
            nested_data = validated_data.pop('nodes')
            nested_serializer.update(nested_instance, nested_data)

        return super(NestedAddressSerializer, self).update(instance, validated_data)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'country', 'country_code', 'postcode', 'state', 'state_district',
            'city', 'street', 'state_district'
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
