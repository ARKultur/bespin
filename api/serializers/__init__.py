from rest_framework import serializers
from api.models import *

from api.serializers.utils import create_instance

"""This module stores all the basic serializers for user & authentication management"""


class TwoFactorAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwoFactorAuth
        fields = ['enabled', 'method']


class AuthSerializer(serializers.ModelSerializer):
    two_factor = TwoFactorAuthSerializer(many=False, read_only=False)

    class Meta:
        model = Auth
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'last_login', 'two_factor', 'date_joined', 'password'
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            instance.set_password(value) if attr == 'password' else setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation

    def create(self, validated_data):
        two_factor = create_instance(TwoFactorAuth, validated_data, 'two_factor')
        return Auth.objects.get_or_create(two_factor=two_factor, **validated_data)


class CustomerSerializer(serializers.ModelSerializer):
    auth = AuthSerializer(many=False, read_only=False)

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        object_data = data.pop('auth')
        validated_data['auth'], created = Auth.objects.get_or_create(role=1,
                is_staff=False, is_superuser=False, **object_name)
        return Admin.objects.get_or_create(**validated_data)


class AdminSerializer(serializers.ModelSerializer):
    auth = AuthSerializer(many=False, read_only=False)

    class Meta:
        model = Admin
        fields = '__all__'

    def create(self, validated_data):
        object_data = data.pop('auth')
        validated_data['auth'], created = Auth.objects.get_or_create(role=2,
                is_staff=False, is_superuser=False, **object_name)
        return Admin.objects.get_or_create(**validated_data)
