from django.db.models import Count, Case, When
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter

from common.views.mixins import ListViewSet, CRUViewSet
from organizations.backends import MyOrganization
from organizations.filters import OrganisationFilter
from organizations.models.organizations import Organization
from organizations.permissions import IsMyOrganization
from organizations.serializars.api import organizations


@extend_schema_view(
    list=extend_schema(summary='Список організацій', tags=['Словники']),
)
class OrganizationSearchListView(ListViewSet):
    queryset = Organization.objects.all()
    serializer_class = organizations.OrganizationSearchListSerializer


@extend_schema_view(
    list=extend_schema(summary='Список організацій', tags=['Організація']),
    retrieve=extend_schema(summary='Детальна інформація про організацію',
                           tags=['Організація']),
    create=extend_schema(summary='Створити організацію', tags=['Організація']),
    update=extend_schema(summary='Змінити дані організації', tags=['Організація']),
    partial_update=extend_schema(summary='Частково змінити дані організації',
                                 tags=['Організація']),
)
class OrganizationView(CRUViewSet):
    permission_classes = [IsMyOrganization, ]
    queryset = Organization.objects.all()
    serializer_class = organizations.OrganizationListSerializer

    multi_serializer_class = {
        'list': organizations.OrganizationListSerializer,
        'retrieve': organizations.OrganizationRetrieveSerializer,
        'create': organizations.OrganizationCreateSerializer,
        'update': organizations.OrganizationUpdateSerializer,
        'partial_update': organizations.OrganizationUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch')

    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
        MyOrganization,
    )

    search_fields = ('name',)
    filterset_class = OrganisationFilter
    ordering = ('name', 'id',)

    def get_queryset(self):
        queryset = Organization.objects.select_related(
            'director',
        ).prefetch_related(
            'employees',
            'groups',
        ).annotate(
            pax=Count('employees', distinct=True),
            groups_count=Count('groups', distinct=True),
            can_manage=Case(
                When(director=self.request.user, then=True),
                default=False
            )
        )

        return queryset
