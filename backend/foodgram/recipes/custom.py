from django.shortcuts import get_object_or_404

from recipes.models import IngredientsInRecipe, Recipe
from tags.models import Tag


def tagsonly(self, obj):
    tags = self.initial_data.get('tags')
    for tag_id in tags:
        obj.tags.add(get_object_or_404(Tag, pk=tag_id))


def customsave(obj, validated_data):
    ingredients = validated_data.pop('ingredient')
    for ingredient in ingredients:
        IngredientsInRecipe.objects.create(
            recipe=obj,
            ingredient_id=ingredient.get('id'),
            amount=ingredient.get('amount')
        )


def add_favorite_or_cart(self, request, pk, serialtype):
    user = request.user
    recipe = get_object_or_404(Recipe, id=pk)

    data = {
        'user': user.id,
        'recipe': recipe.id,
    }
    serializer = serialtype(
        data=data,
        context={'request': request}
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer


def delete_favorite_or_cart(self, request, pk, model):
    user = request.user
    recipe = get_object_or_404(Recipe, id=pk)
    favorite_or_shop_item = get_object_or_404(
        model, user=user, recipe=recipe
    )
    favorite_or_shop_item.delete()
