from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Organization(models.Model):
    name = models.CharField('Назва', max_length=255)
    director = models.ForeignKey(User, models.RESTRICT, 'organization_director',
                                 verbose_name='Директор')
    employees = models.ManyToManyField(User, 'organization_employees',
                                       verbose_name='Працівники',
                                       blank=True)

    class Meta:
        verbose_name = 'Організація'
        verbose_name_plural = 'Організації'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.pk})'



