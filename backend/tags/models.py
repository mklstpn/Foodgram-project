from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            verbose_name='Название тэга')
    color = models.CharField(max_length=50,
                             verbose_name='Цвет тэга')
    slug = models.SlugField(max_length=255, unique=True,
                            verbose_name='Уникальный слаг')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name
