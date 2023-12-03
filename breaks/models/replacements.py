from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


#
class GroupInfo(models.Model):
    group = models.OneToOneField(
        'organizations.Group', models.CASCADE, related_name='breaks_info',
        verbose_name='Група', primary_key=True
    )
    min_active = models.PositiveSmallIntegerField(
        'Мінімальна кількість активних працівників', null=True, blank=True
    )
    break_start = models.TimeField('Початок обіду', null=True, blank=True)
    break_end = models.TimeField('Кінець обіду', null=True, blank=True)
    break_max_duration = models.PositiveSmallIntegerField('Максимальна тривалість обіду',
                                                          null=True, blank=True)

    class Meta:
        verbose_name = 'Параметр обідніх перерв'
        verbose_name_plural = 'Параметри обідніх перерв'

    def __str__(self):
        return f'{self.group}'


class Replacement(models.Model):
    group = models.ForeignKey(
        'breaks.GroupInfo', models.CASCADE, 'replacements',
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
