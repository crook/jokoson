from rest_framework import permissions


class ModelPermission(permissions.BasePermission):
    """
    """

    def has_permission(self, request, view):
        # IsAdminOrReadOnly permission
        if ((request.user and request.user.is_staff) or
                request.method in permissions.SAFE_METHODS):
            return True

        return False


class ManufacturePermission(permissions.BasePermission):
    """
    """

    def has_permission(self, request, view):
        # IsAdminOrReadOnly permission
        if ((request.user and request.user.is_staff) or
                request.method in permissions.SAFE_METHODS):
            return True

        return False


class EquipPermission(permissions.BasePermission):
    """
    """

    def has_permission(self, request, view):
        # IsAdminOrReadOnly permission
        if ((request.user and request.user.is_staff) or
                request.method in permissions.SAFE_METHODS):
            return True

        return False


class OrderPermission(permissions.BasePermission):
    """
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            if request.user.is_authenticated:
                if ('tenant' in request.data and
                        request.user.username != request.data['tenant']):
                    return False
                else:
                    return True

        return False
