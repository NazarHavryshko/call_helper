from django.db.models import Count, Case, When, Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend

from common.views.mixins import CRUDViewSet
from organizations.backends import OwnByOrganization, MyGroup
from organizations.filters import EmployeeFilter, GroupFilter
from organizations.models.grups import Group
from organizations.models.organizations import Employee
from organizations.permissions import IsMyGroup
from organizations.serializars.api import group


@extend_schema_view(
    list=extend_schema(summary='Список груп',
                       tags=['Організація: Групи']),
    retrieve=extend_schema(summary='Детальна інформація групи',
                           tags=['Організація: Групи']),
    create=extend_schema(summary='Створити групу',
                         tags=['Організація: Групи']),
    update=extend_schema(summary='Змінити групу',
                         tags=['Організація: Групи']),
    partial_update=extend_schema(summary='Частково змінити групу',
                                 tags=['Організація: Групи'])
)
class GroupView(CRUDViewSet):
    queryset = Group.objects.all()
    serializer_class = group.GroupListSerializer

    permission_classes = [IsMyGroup]

    multi_serializer_class = {
        'list': group.GroupListSerializer,
        'retrieve': group.GroupRetrieveSerializer,
        'create': group.GroupCreateSerializer,
        'update': group.GroupUpdateSerializer,
        'partial_update': group.GroupUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch')

    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
        MyGroup,
    )
    search_fields = ('name',)
    filterset_class = GroupFilter
    ordering = ('name', 'id')

    def get_queryset(self):
        queryset = Group.objects.select_related(
            'manager',
        ).prefetch_related(
            'organization',
            'organization__director',
            'members',
        ).annotate(
            pax=Count('members', distinct=True),
            can_manage=Case(
                When(
                    Q(manager__user=self.request.user) |
                    Q(organization__director=self.request.user),
                    then=True),
                default=False
            ),
            is_member=Case(
                When(Q(members_info__employee__user=self.request.user), then=True),
                default=False)

        )

        return queryset
