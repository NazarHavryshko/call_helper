from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from config import settings

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


class DateMixin(models.Model):
    """
    Add info when data is created and updated in DataBase
    """
    created_at = models.DateTimeField('Created at', null=True, blank=True)
    updated_at = models.DateTimeField('Updated at', null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(DateMixin, self).save(*args, **kwargs)


class InfoMixin(DateMixin):
    """
    Add info on who created and updated data in DataBase
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL,
        related_name='created_%(app_label)s_%(class)s',
        verbose_name='Created by', null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL,
        related_name='updated_%(app_label)s_%(class)s',
        verbose_name='Updated by', null=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        from crum import get_current_user

        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_at = user
        self.updated_at = user
        super().save(*args, **kwargs)
