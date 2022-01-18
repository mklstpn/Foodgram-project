from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    color = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name
