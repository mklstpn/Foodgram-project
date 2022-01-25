from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from tags.serializers import TagSerializer
from users.models import CustomUser
from users.serializers import CurrentUserSerializer
from .custom import add_ingredients, add_tags
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
        source='amounts', read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time', 'id', 'ingredients')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorites.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Cart.objects.filter(
            user=request.user, recipe=obj).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError({
                    'ingredient': 'Нельзя добавить игредиент 2 раза'
                })
            ingredients_list.append(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError({
                    'amount': 'Количество не может быть меньше нуля'
                })

        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError({
                'cooking_time': 'Время не может быть меньше нуля'
            })

        return data

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients = validated_data.pop('ingredient')
        recipe = Recipe.objects.create(image=image, **validated_data)
        add_tags(self, recipe)
        add_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        instance.ingredient.clear()
        ingredients = validated_data.pop('ingredient')
        add_tags(self, instance)
        add_ingredients(instance, ingredients)
        return super().update(instance, validated_data)


class RepresentationSerializer(serializers.ModelSerializer):
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

        if request.method == 'POST' and favorite_exists:
            raise serializers.ValidationError(
                'Уже в избранном'
            )

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RepresentationSerializer(
            instance.recipe,
            context=context).data


class CartSerializer(FavoritesSerializer):
    class Meta(FavoritesSerializer.Meta):
        model = Cart
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        purchase_exists = Cart.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()

        if request.method == 'POST' and purchase_exists:
            raise serializers.ValidationError(
                'Уже в списке покупок'
            )

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RepresentationSerializer(
            instance.recipe,
            context=context).data
