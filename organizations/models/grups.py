from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from common.models.mixins import InfoMixin

User = get_user_model()


class Group(InfoMixin):
    organization = models.ForeignKey('Organization', models.CASCADE, 'groups',
                                     verbose_name='Організація')
    name = models.CharField('Назва', max_length=255)
    manager = models.ForeignKey('Employee', models.RESTRICT, 'groups_manager',
                                verbose_name='Менеджер')
    members = models.ManyToManyField(
        'Employee', 'groups_members',
        verbose_name='Учасники групи',
        blank=True, through='Member',
    )

    class Meta:
        verbose_name = 'Група'
        verbose_name_plural = 'Групи'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Member(models.Model):
    group = models.ForeignKey(
        'Group', models.CASCADE, 'members_info',
    )
    employee = models.ForeignKey(
        'Employee', models.CASCADE, 'group_info',
    )
    date_joined = models.DateField('Date joined', default=timezone.now)

    class Meta:
        verbose_name = 'Учасник групи'
        verbose_name_plural = 'Учасники групи'
        ordering = ('-date_joined',)
        unique_together = (('group', 'employee',),)

    def __str__(self):
        return f'Member {self.employee} in Group {self.group}'
