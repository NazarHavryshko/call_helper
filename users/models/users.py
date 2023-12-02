from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.models.managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField('Пошта', unique=True, null=True, blank=True)
    username = models.CharField('Нікнейм', max_length=64, null=True, blank=True, unique=True)
    phone_number = PhoneNumberField('Телефон', unique=True, null=True, blank=True)

    # USERNAME_FIELD = ''
    # REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name} ({self.pk})'
