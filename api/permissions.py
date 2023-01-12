from rest_framework import permissions

import logging

from api.models import Auth, Customer, Admin
from api.models.domains import Address, Node

"""this module stores the various authorization middlewares used throughout the project

(user should already be authenticated when going through these)
"""

class MethodOnly(permissions.BasePermission):
    SAFE_METHODS = []

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return True
        return False


class DeleteOnly(MethodOnly):
    SAFE_METHODS = ['DELETE']


class ReadOnly(MethodOnly):
    SAFE_METHODS = ['GET']


class PostOnly(MethodOnly):
    SAFE_METHODS = ['POST']


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Auth):
            return obj.id == request.user.id

        if isinstance(obj, (Customer, Admin)):
            return obj.auth.id == request.user.id

        if isinstance(obj, Address):
            return obj.owner.auth.id == request.user.id

        if isinstance(obj, Node):
            return obj.address.owner.auth.id == request.user.id

        logging.getLogger(__name__).warn(f'IsOwner permissions: {type(obj)} did not reach anything')
        return False


def user_has_role(request, role: str) -> bool:
    user_roles = ['placeholder', 'customer', 'admin']
    return user_roles[request.user.role] == role


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request, 'admin')

    def has_object_permission(self, request, view, obj):
        return user_has_role(request, 'admin')


class IsNotAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return not user_has_role(request, 'admin')

    def has_object_permission(self, request, view, obj):
        return not user_has_role(request, 'admin')


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request, 'customer')

    def has_object_permission(self, request, view, obj):
        return user_has_role(request, 'customer')


class IsNotCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return not user_has_role(request, 'customer')

    def has_object_permission(self, request, view, obj):
        return not user_has_role(request, 'customer')
