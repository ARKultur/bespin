from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_400_BAD_REQUEST,
        HTTP_200_OK,
        HTTP_403_FORBIDDEN,
        HTTP_404_NOT_FOUND,
        HTTP_406_NOT_ACCEPTABLE
        )

from api.serializers import *
from api.serializers.domains import *

from api.permissions import IsAdmin, IsOwner, IsCustomer, PostOnly

"""This module stores the generic viewsets used when basic CRUD is required

- TwoFactorViewset: 2FA class CRUD
- AuthViewset: Auth class CRUD
- RegisterViewset: Customer creation route
- CustomerViewset: Customer CRUD
- AdminViewset: Admin CRUD
- NodeViewset: Node class CRUD
- AddressViewset: Address class CRUD (no preloaded data)
"""


class TwoFactorViewset(viewsets.ModelViewSet):
    queryset = TwoFactorAuth.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsOwner]
    authentication_classes = [TokenAuthentication]
    serializer_class = TwoFactorAuthSerializer


class RegisterViewset(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [PostOnly]
    authentication_classes = []
    serializer_class = CustomerSerializer


class CustomerViewset(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = []
    authentication_classes = []
    serializer_class = CustomerSerializer


class AdminViewset(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    authentication_classes = [TokenAuthentication]
    serializer_class = AdminSerializer


class AuthViewset(viewsets.ModelViewSet):
    queryset = Auth.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsOwner]
    authentication_classes = [TokenAuthentication]
    serializer_class = AuthSerializer


class NodeViewset(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsOwner]
    authentication_classes = [TokenAuthentication]
    serializer_class = NodeSerializer


class AddressViewset(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsOwner]
    authentication_classes = [TokenAuthentication]
    serializer_class = AddressSerializer
