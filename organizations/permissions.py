from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsMyOrganization(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.director == request.user:
            return True

        if request.method in SAFE_METHODS:
            return obj.employees.filter(user=request.user).exists()

        return False


class IsColleagues(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.organization.director == request.user:
            return True

        if request.method in SAFE_METHODS:
            return obj.organization.employees.filter(user=request.user).exists()

        return False


class IsMyGroup(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.organization.director == request.user:
            return True

        if request.method in SAFE_METHODS:
            return obj.organization.employees.filter(user=request.user).exists()

        return False
