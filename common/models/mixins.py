from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseDictModelMixin(models.Model):
    code = models.CharField('Код', max_length=16, primary_key=True)
    name = models.CharField('Назва', max_length=32)
    sort = models.PositiveSmallIntegerField('Сортування', null=True, blank=True)
    is_active = models.BooleanField('Активність', default=True)

    class Meta:
        ordering = ('sort',)
        abstract = True

    def __str__(self):
        return f'{self.code} ({self.name})'
