from rest_framework.permissions import BasePermission


class IsOpsOrParent(BasePermission):
    def has_permission(self, request, view):
        """
         using custom header RBAC for dev
        """
        role = request.headers.get("X-ROLE")
        return role in ["OPS", "PARENT"]
