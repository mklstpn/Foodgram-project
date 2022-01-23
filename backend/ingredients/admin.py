from django.contrib import admin

from .models import Ingredient


class IngredientAdmin(admin.ModelAdmin):
    list = ('name', 'measurement_unit')


admin.site.register(Ingredient, IngredientAdmin)
