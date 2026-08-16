from rest_framework.permissions import BasePermission


class IsAdministrator(BasePermission):
    message = "Only administrators can create user accounts."

    def has_permission(self, request, view) -> bool:
        user = request.user

        if not user.is_authenticated:
            return False

        return user.is_superuser or user.groups.filter(name="Administrator").exists()
