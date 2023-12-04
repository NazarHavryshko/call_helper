from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from common.models.mixins import InfoMixin

User = get_user_model()


class Organization(InfoMixin):
    name = models.CharField('Назва', max_length=255)
    director = models.ForeignKey(User, models.RESTRICT, 'organizations_director',
                                 verbose_name='Директор')
    employees = models.ManyToManyField(
        User, 'organizations_employees',
        verbose_name='Працівники',
        blank=True, through='Employee'
    )

    class Meta:
        verbose_name = 'Організація'
        verbose_name_plural = 'Організації'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Employee(models.Model):
    organization = models.ForeignKey(
        'Organization', models.CASCADE, 'employees_info',
    )
    user = models.ForeignKey(
        User, models.CASCADE, 'organization_info',
    )
    position = models.ForeignKey(
        'Position', models.RESTRICT, 'employees',
    )
    date_joined = models.DateField('Date joined', default=timezone.now)

    class Meta:
        verbose_name = 'Працівник'
        verbose_name_plural = 'Працівники'
        ordering = ('-date_joined',)
        unique_together = (('organization', 'user', ),)

    def __str__(self):
        return f'Employee {self.user}'
