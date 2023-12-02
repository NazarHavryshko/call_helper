from django.contrib.auth import get_user_model
from django.db import models

from breaks.models.dicts import BreakStatus
from constants import BREAK_CREATED_STATUS

User = get_user_model()


class Break(models.Model):
    replacement = models.ForeignKey('breaks.Replacement', models.CASCADE, 'breaks',
                                    verbose_name='Зміна')
    employees = models.ForeignKey(User, models.CharField, 'breaks',
                                  verbose_name='Працівник', )
    break_start = models.TimeField('Початок обіду', null=True, blank=True)
    break_end = models.TimeField('Кінець обіду', null=True, blank=True)
    status = models.ForeignKey('breaks.BreakStatus', models.RESTRICT, verbose_name='Статус', blank=True, null=True)

    class Meta:
        verbose_name = 'Обідяна перерва'
        verbose_name_plural = 'Обідяні перерви'
        ordering = ('-replacement__date', 'break_start')

    def __str__(self):
        return f'Обід працівника {self.employees} ({self.pk})'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = BreakStatus.objects.get(code=BREAK_CREATED_STATUS)
        return super().save(*args, **kwargs)
