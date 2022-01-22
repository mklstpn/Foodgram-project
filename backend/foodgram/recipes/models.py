from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag
from users.models import CustomUser

User = CustomUser


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    image = models.ImageField(upload_to='recipes/')
    text = models.TextField(max_length=1255)
    cooking_time = models.IntegerField()
    ingredient = models.ManyToManyField(
        Ingredient, through='IngredientsInRecipe')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='amounts')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='amounts')
    amount = models.PositiveIntegerField()

    class Meta:
        unique_together = ('recipe', 'ingredient')
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='recipe_ingredients_unique',
            )
        ]


class Favorites(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,  related_name='favorites_user')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,  related_name='favorite_recipe')

    class Meta:
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
        User, on_delete=models.CASCADE, related_name='carts')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='carts')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='purchase_user_recipe_unique'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в списке покупок {self.user}'
