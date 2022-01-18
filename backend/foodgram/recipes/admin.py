from django.contrib import admin

from .models import Cart, Favorites, IngredientsInRecipe, Recipe


class IngredientsInRecipeAdmin(admin.TabularInline):
    model = IngredientsInRecipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'image', 'text',
                    'cooking_time')

    inlines = [
        IngredientsInRecipeAdmin,
    ]


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Favorites, FavoriteAdmin)
