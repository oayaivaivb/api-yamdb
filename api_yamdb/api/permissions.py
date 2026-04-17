"""Модуль с классами разрешений (permissions) для API."""

from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешение только для администраторов."""

    def has_permission(self, request, view):
        """Проверка прав на уровне запроса."""
        return (request.user and request.user.is_authenticated
                and request.user.is_admin())


class IsAdminOrReadOnly(IsAdmin):
    """Чтение для всех, запись только для администраторов."""

    def has_permission(self, request, view):
        """Проверка прав на уровне запроса."""
        return (request.method in permissions.SAFE_METHODS
                or super().has_permission(request, view))


class IsAuthorOrModeratorOrAdmin(IsAdminOrReadOnly):
    """Разрешение для автора, модератора или администратора."""

    def has_permission(self, request, view):
        """Проверка прав на уровне запроса."""
        return (super().has_permission(request, view)
                or (request.user and request.user.is_authenticated))

    def has_object_permission(self, request, view, obj):
        """Проверка прав на уровне объекта."""
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author
                or request.user.is_moderator()
                or request.user.is_admin())
