"""This module stores the generic viewsets used when basic CRUD is required

- AuthViewset: Auth class CRUD
- RegisterViewset: Customer creation route
- CustomerViewset: Customer CRUD
- AdminViewset: Admin CRUD
- NodeViewset: Node class CRUD
- AddressViewset: Address class CRUD (no preloaded data)
"""

from typing import List
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication

from api.serializers import AdminSerializer, CustomerSerializer, AuthSerializer
from api.serializers.domains import NodeSerializer, AddressSerializer

from api.models import Admin, Auth, Customer
from api.models.domains import Address, Node

from api.permissions import IsAdmin, IsOwner, PostOnly


class RegisterViewset(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors

    """
        RegisterViewset:
            Binding to CustomerSerializer in order to register new account
    """

    queryset = Customer.objects.all()
    permission_classes = [PostOnly]
    authentication_classes: List[type[TokenAuthentication]] = []
    serializer_class = CustomerSerializer

class CustomerViewset(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors

    """
        CustomerViewset
            CRUD operations for Customer model (encompasses Auth model as well)
    """

    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated & IsAdmin | IsOwner]
    authentication_classes = [TokenAuthentication]
    serializer_class = CustomerSerializer


class AdminViewset(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors

    """
       AdminViewset
            CRUD operations for Admin model (encompasses Auth model as well)
    """

    queryset = Admin.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    authentication_classes = [TokenAuthentication]
    serializer_class = AdminSerializer


class AuthViewset(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors

    """
        AuthViewset
            currently unused but might be useful later
    """

    queryset = Auth.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsOwner]
    authentication_classes = [TokenAuthentication]
    serializer_class = AuthSerializer


class NodeViewset(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors

    """
        NodeViewset
            CRUD for Node models
    """
    queryset = Node.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsOwner]
    authentication_classes = [TokenAuthentication]
    serializer_class = NodeSerializer


class AddressViewset(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors

    """
        AddressViewset
            CRUD for Address models
    """

    queryset = Address.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsOwner]
    authentication_classes = [TokenAuthentication]
    serializer_class = AddressSerializer
