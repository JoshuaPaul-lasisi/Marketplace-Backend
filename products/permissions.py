from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsVendorOrReadOnly(BasePermission):
    """
    Only vendors can create/update/delete products.
    Customers and unauthenticated users can only read.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS → always allowed
        if request.method in SAFE_METHODS:
            return True

        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Only vendors can modify
        return request.user.user_type == "vendor"

    def has_object_permission(self, request, view, obj):
        # Read-only access for everyone
        if request.method in SAFE_METHODS:
            return True

        # Vendors can only modify their own products
        return obj.vendor == request.user