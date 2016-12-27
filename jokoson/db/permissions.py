from rest_framework import permissions


class CategoryPermission(permissions.BasePermission):
    """
    """

    def has_permission(self, request, view):
        if (not request.user.is_staff and
                request.method not in permissions.SAFE_METHODS):
            return False
        return True


class VendorPermission(permissions.BasePermission):
    """
    """

    def has_permission(self, request, view):
        if (not request.user.is_staff and
                request.method not in permissions.SAFE_METHODS):
            return False
        return True


class EquipPermission(permissions.BasePermission):
    """
    """

    def has_permission(self, request, view):
        if (not request.user.is_staff and
                request.method not in permissions.SAFE_METHODS):
            return False
        return True


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
