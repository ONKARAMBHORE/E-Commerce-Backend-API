from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"


class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "CUSTOMER"


class IsSeller(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "SELLER"


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user