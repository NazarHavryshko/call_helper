from django.db import models


class Profile(models.Model):
    users = models.OneToOneField('users.User', on_delete=models.CASCADE,
                                 related_name='profile',
                                 verbose_name='Користувач',
                                 primary_key=True)
    telegram_id = models.CharField('Telegram ID', max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = 'Профіль користувача'
        verbose_name_plural = 'Профілі користувачів'

    def __str__(self):
        return f'{self.users} ({self.pk})'



