from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class MyOrganization(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(
            Q(director=user) | Q(employees=user)
        ).distinct()


class OwnByOrganization(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        org_id = request.parser_context['kwargs'].get('pk')
        if org_id is not None:
            return queryset.filter(organization_id=org_id)
        return queryset.none()


class MyGroup(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(
            Q(organization__director=user) | Q(organization__employees=user)
        ).distinct()
