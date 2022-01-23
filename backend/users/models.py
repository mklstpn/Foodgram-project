from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(null=False, unique=True,
                              verbose_name='email')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return self.email


User = CustomUser


class Follow(models.Model):
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following', verbose_name='автор')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower', verbose_name='фолловер')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='follow_unique')
        ]

    def __str__(self):
        return f"{self.user} follows {self.following}"
