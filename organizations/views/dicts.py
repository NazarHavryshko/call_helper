from drf_spectacular.utils import extend_schema_view, extend_schema

from common.views.mixins import DictListMixin
from organizations.models.dicts import Position


@extend_schema_view(
    list=extend_schema(summary='Список посад',
                       tags=['Словники']),
)
class PositionView(DictListMixin):
    queryset = Position.objects.filter(is_active=True)

