from django.contrib.auth import get_user_model
from django.db import models

from common.models.mixins import BaseDictModelMixin

User = get_user_model()


class ReplacementStatus(BaseDictModelMixin):
    class Meta:
        verbose_name = 'Cтатус зміни'
        verbose_name_plural = 'Статуси змін'


class BreakStatus(BaseDictModelMixin):
    class Meta:
        verbose_name = 'Cтатус обіду'
        verbose_name_plural = 'Статуси обідів'
