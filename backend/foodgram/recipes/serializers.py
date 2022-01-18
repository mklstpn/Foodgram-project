from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from tags.models import Tag
from tags.serializers import TagSerializer
from users.models import CustomUser
from users.serializers import CurrentUserSerializer

from .models import Cart, Favorites, IngredientsInRecipe, Recipe


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = CurrentUserSerializer(read_only=True)
    ingredients = IngredientsInRecipeSerializer(
        source='ingredientinrecipe_set', read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('__all__')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorites.objects.filter(user=request.user,
                                        recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Cart.objects.filter(user=request.user,
                                   recipe=obj).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredient')
        ingredients_set = set()
        for ingredient in ingredients:
            if int(ingredient.get('amount')) <= 0:
                raise serializers.ValidationError(
                    ('Количство должно быть больше 0')
                )
            id = ingredient.get('id')
            if id in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторятся.'
                )
            ingredients_set.add(id)
        data['ingredient'] = ingredients

        return data

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients = validated_data.pop('ingredient')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags = self.initial_data.get('tags')

        for tag_id in tags:
            recipe.tags.add(get_object_or_404(Tag, pk=tag_id))

        for ingredients in ingredients:
            IngredientsInRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredients.get('id'),
                amount=ingredients.get('amount')
            )

        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        tags = self.initial_data.get('tags')

        for tag_id in tags:
            instance.tags.add(get_object_or_404(Tag, pk=tag_id))

        IngredientsInRecipe.objects.filter(recipe=instance).delete()
        for ingredient in validated_data.get('ingredient'):
            ingredients_amounts = IngredientsInRecipe.objects.create(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
            ingredients_amounts.save()

        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.save()

        return instance


class FollowerRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoritesSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())

    class Meta:
        model = Favorites
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        favorite_exists = Favorites.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()

        if request.method == 'GET' and favorite_exists:
            raise serializers.ValidationError(
                'Уже в избранном'
            )

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FollowerRecipeSerializer(
            instance.recipe,
            context=context).data


class CartSerializer(FavoritesSerializer):
    class Meta(FavoritesSerializer.Meta):
        model = Cart

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        purchase_exists = Cart.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()

        if request.method == 'GET' and purchase_exists:
            raise serializers.ValidationError(
                'Уже в списке покупок'
            )

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FollowerRecipeSerializer(
            instance.recipe,
            context=context).data
