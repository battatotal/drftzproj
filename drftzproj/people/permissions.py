from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class OnlyOneProfile(permissions.BasePermission):
    #Разрешение на создание только одного профиля для юзера

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
            and not hasattr(request.user, 'profile')
        )
