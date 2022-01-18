from django.db.models import Exists, OuterRef
from django.http.response import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import Cart, Favorites, IngredientsInRecipe, Recipe
from .pagination import CustomPagination
from .permissions import IsOwnerOrAdminOrReadOnly
from .serializers import CartSerializer, FavoritesSerializer, RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Recipe.objects.all()

        queryset = Recipe.objects.annotate(
            is_favorited=Exists(Favorites.objects.filter(
                user=user, recipe_id=OuterRef('pk')
            )),
            is_in_shopping_cart=Exists(Cart.objects.filter(
                user=user, recipe_id=OuterRef('pk')
            ))
        )

        if self.request.GET.get('is_favorited'):
            return queryset.filter(is_favorited=True)
        elif self.request.GET.get('is_in_shopping_cart'):
            return queryset.filter(is_in_shopping_cart=True)

        return queryset

    @action(detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        data = {
            'user': user.id,
            'recipe': recipe.id,
        }
        serializer = FavoritesSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorites = get_object_or_404(
            Favorites, user=user, recipe=recipe
        )
        favorites.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        data = {
            'user': user.id,
            'recipe': recipe.id,
        }
        serializer = CartSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorites = get_object_or_404(
            Cart, user=user, recipe=recipe
        )
        favorites.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = user.carts.all()
        list = {}
        for item in shopping_cart:
            recipe = item.recipe
            ingredients = IngredientsInRecipe.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in list:
                    list[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    list[name]['amount'] = (
                        list[name]['amount'] + amount
                    )

        shopping_list = []
        for item in list:
            shopping_list.append(f'{item} - {list[item]["amount"]} '
                                 f'{list[item]["measurement_unit"]} \n')
        response = HttpResponse(shopping_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="cart.txt"'

        return response
