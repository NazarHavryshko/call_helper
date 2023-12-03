from django.contrib.auth import get_user_model

from common.models.mixins import BaseDictModelMixin

User = get_user_model()


class Position(BaseDictModelMixin):
    class Meta:
        verbose_name = 'Посада'
        verbose_name_plural = 'Посади'
