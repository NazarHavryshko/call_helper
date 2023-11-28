from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Replacement(models.Model):
    group = models.ForeignKey(
        'breaks.Group', models.CASCADE, 'replacements',
        verbose_name='Група'
    )
    date = models.DateField('Дата зміни')
    breaks_start = models.TimeField('Початок обіду')
    breaks_end = models.TimeField('Кінець обіду')
    breaks_max_duration = models.PositiveSmallIntegerField('Максимальна тривалість обіду')

    class Meta:
        verbose_name = 'Зміна'
        verbose_name_plural = 'Зміни'
        ordering = ('-date',)

    def __str__(self):
        return f'Зміна № {self.pk} для {self.group}'


class ReplacementEmployee(models.Model):
    employee = models.ForeignKey(
        User, models.CASCADE, 'replacements',
        verbose_name='Працівник'
    )
    replacement = models.ForeignKey(
        'breaks.Replacement', models.CASCADE, 'employees',
        verbose_name='Зміна'
    )
    status = models.ForeignKey(
        'breaks.ReplacementStatus', models.RESTRICT, 'replacement_employees',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Зміна - працівник'
        verbose_name_plural = 'Зміни - працівники'

    def __str__(self):
        return f'Зміна {self.replacement} для {self.employee}'
