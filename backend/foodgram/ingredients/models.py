from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    measurement_unit = models.CharField(max_length=10)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'
