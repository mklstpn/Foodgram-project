from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag
from users.models import CustomUser

User = CustomUser


class Recipe(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название рецепта')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='Автор')
    image = models.ImageField(upload_to='recipes/',
                              verbose_name='Фото рецепта')
    text = models.TextField(max_length=1255, verbose_name='Текстовое описание')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления')
    ingredient = models.ManyToManyField(
        Ingredient, through='IngredientsInRecipe', verbose_name='Ингридиенты')
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Тэги')
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата публикации')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='amounts', verbose_name='Ингредиент')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='amounts', verbose_name='Рецепт')
    amount = models.PositiveIntegerField(verbose_name='Количество ингредиента')

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        unique_together = ('recipe', 'ingredient')
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='recipe_ingredients_unique',
            )
        ]


class Favorites(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites',
        verbose_name='Рецепты в избранном')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite_user_recept_unique'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='carts',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='carts',
        verbose_name='Рецепты в корзине')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='purchase_user_recipe_unique'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в списке покупок {self.user}'
