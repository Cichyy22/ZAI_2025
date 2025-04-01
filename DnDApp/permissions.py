from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permisja, która pozwala dostęp tylko właścicielowi postaci lub administratorowi.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if obj.user == request.user:
            return True
        return False