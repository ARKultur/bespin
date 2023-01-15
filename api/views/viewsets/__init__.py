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


class RegisterViewset(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [PostOnly]
    authentication_classes: List[type[TokenAuthentication]] = []
    serializer_class = CustomerSerializer

class CustomerViewset(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated & IsAdmin | IsOwner]
    authentication_classes = [TokenAuthentication]
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
