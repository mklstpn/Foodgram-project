from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField('email', null=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.email


User = CustomUser


class Follow(models.Model):
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='follow_unique')
        ]

    def __str__(self):
        return f"{self.user} follows {self.following}"
