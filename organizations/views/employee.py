from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend

from common.views.mixins import CRUDViewSet
from organizations.backends import OwnByOrganization
from organizations.filters import EmployeeFilter
from organizations.models.organizations import Employee
from organizations.permissions import IsColleagues
from organizations.serializars.api import employees


@extend_schema_view(
    list=extend_schema(summary='Список cпівробітників організації',
                       tags=['Організація: Співробітники']),
    retrieve=extend_schema(summary='Детальна інформація cпівробітника організації',
                           tags=['Організація: Співробітники']),
    create=extend_schema(summary='Створити cпівробітника організації',
                         tags=['Організація: Співробітники']),
    update=extend_schema(summary='Змінити cпівробітника організації',
                         tags=['Організація: Співробітники']),
    partial_update=extend_schema(summary='Частково змінити cпівробітника організації',
                                 tags=['Організація: Співробітники']),
    destroy=extend_schema(summary='Видалити cпівробітника організації',
                          tags=['Організація: Співробітники']),
)
class EmployeeView(CRUDViewSet):
    queryset = Employee.objects.all()
    serializer_class = employees.EmployeeListSerializer

    permission_classes = [IsColleagues]

    multi_serializer_class = {
        'list': employees.EmployeeListSerializer,
        'retrieve': employees.EmployeeRetrieveSerializer,
        'create': employees.EmployeeCreateSerializer,
        'update': employees.EmployeeUpdateSerializer,
        'partial_update': employees.EmployeeUpdateSerializer,
        'destroy': employees.EmployeeDestroySerializer,
    }

    lookup_url_kwarg = 'employee_id'
    http_method_names = ('get', 'post', 'patch', 'delete')

    filter_backends = (
        BaseFilterBackend,
        OrderingFilter,
        SearchFilter,
        OwnByOrganization,
    )
    search_fields = ('name',)
    filterset_class = EmployeeFilter
    ordering = ('position', 'date_joined', 'id')

    def get_queryset(self):
        queryset = Employee.objects.select_related(
            'user',
            'position',
        ).prefetch_related(
            'organization',
        )

        return queryset


