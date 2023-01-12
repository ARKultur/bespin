from rest_framework import serializers
from argon2 import PasswordHasher
from api.models import *

from api.serializers.utils import create_instance

"""This module stores all the basic serializers for user & authentication management"""


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'last_login', 'date_joined', 'password'
        ]

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            passwd = validated_data['password']
            validated_data['password'] = PasswordHasher().hash(passwd)

        return super(AuthSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation

    def create(self, validated_data):
        if 'password' in validated_data:
            passwd = validated_data['password']
            validated_data.pop('password')
            validated_data['password'] = PasswordHasher().hash(passwd)

        return Auth.objects.create(**validated_data)


class CustomerSerializer(serializers.ModelSerializer):
    auth = AuthSerializer(many=False, read_only=False)

    class Meta:
        model = Customer
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'auth' in validated_data:
            nested_serializer = self.fields['auth']
            nested_instance = instance.auth
            nested_data = validated_data.pop('auth')
            nested_serializer.update(nested_instance, nested_data)
        return super(CustomerSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        auth_data = validated_data.get('auth')
        auth_data['role'] = 1
        auth_data['is_superuser'] = False
        auth_data['is_staff'] = False
        auth = create_instance(AuthSerializer, validated_data, 'auth')
        return Customer.objects.create(auth=auth, **validated_data)


class AdminSerializer(serializers.ModelSerializer):
    auth = AuthSerializer(many=False, read_only=False)

    class Meta:
        model = Admin
        fields = '__all__'

    def create(self, validated_data):
        auth_data = validated_data.get('auth')
        auth_data['role'] = 2
        auth_data['is_superuser'] = True
        auth_data['is_staff'] = True
        auth = create_instance(AuthSerializer, validated_data, 'auth')
        return Admin.objects.create(auth=auth, **validated_data)

    def update(self, instance, validated_data):
        if 'auth' in validated_data:
            nested_serializer = self.fields['auth']
            nested_instance = instance.auth
            nested_data = validated_data.pop('auth')
            nested_serializer.update(nested_instance, nested_data)
        return super(AdminSerializer, self).update(instance, validated_data)
