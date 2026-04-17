from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешение только для администраторов."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin()
        )


class IsAdminOrReadOnly(IsAdmin):
    """Чтение для всех, запись только для администраторов."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )


class IsAuthorOrModeratorOrAdmin(IsAdminOrReadOnly):
    """Разрешение для автора, модератора или администратора."""

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            or (request.user and request.user.is_authenticated)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator()
            or request.user.is_admin()
        )
