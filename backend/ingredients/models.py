from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Название ингредиента')
    measurement_unit = models.CharField(
        max_length=10, verbose_name='Единицы измерения')

    class Meta:
        ordering = ('name', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'