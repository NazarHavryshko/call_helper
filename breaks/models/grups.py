from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    organization = models.ForeignKey('breaks.Organization', models.CASCADE, 'groups',
                                     verbose_name='Організація')
    name = models.CharField('Назва', max_length=255)
    manager = models.ForeignKey(User, models.RESTRICT, 'group_manager',
                                verbose_name='Менеджер')
    employees = models.ManyToManyField(User, 'grop_employees',
                                       verbose_name='Працівники',
                                       blank=True)
    min_active = models.PositiveSmallIntegerField(
        'Мінімальна кількість активних працівників', null=True, blank=True
    )
    break_start = models.TimeField('Початок обіду', null=True, blank=True)
    break_end = models.TimeField('Кінець обіду', null=True, blank=True)
    break_max_duration = models.PositiveSmallIntegerField('Максимальна тривалість обіду', null=True, blank=True)

    class Meta:
        verbose_name = 'Група'
        verbose_name_plural = 'Групи'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.pk})'