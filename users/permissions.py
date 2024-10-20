from rest_framework.permissions import BasePermission

class IsEmployer(BasePermission):
    """allow access only to employer"""
    def has_permission(self, request, view):
        return request.user and request.user.role == "EMPLOYEER"

class IsEmployee(BasePermission):
    """allow access only to employee"""
    def has_permission(self, request, view):
        return request.user and request.user.role == "EMPLOYEE"