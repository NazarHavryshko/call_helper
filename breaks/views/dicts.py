from drf_spectacular.utils import extend_schema_view, extend_schema

from common.serializers.mixins import DictMixinSerializer
from common.views.mixins import DictListMixin
from breaks.models import dicts


@extend_schema_view(
    list=extend_schema(summary='Статус змін',
                       tags=['Словники']),
)
class ReplacementStatusView(DictListMixin):
    queryset = dicts.ReplacementStatus.objects.filter(is_active=True)


@extend_schema_view(
    list=extend_schema(summary='Статус обідіх перерв',
                       tags=['Словники']),
)
class BreakStatusView(DictListMixin):
    queryset = dicts.BreakStatus.objects.filter(is_active=True)
