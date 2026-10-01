from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    message = "You don't have permission for this."

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_superuser:
            return True
        return False
    
class IsManager(BasePermission):
    message = "You don't have permission for this."

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.role=='M':
            return True
        return False
    
class IsManager_or_superuser(BasePermission):
    message = "You don't have permission for this."

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'M'):
            return True
        return False
