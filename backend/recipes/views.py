from django.db.models import Sum
from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .custom import add_favorite_or_cart, delete_favorite_or_cart
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
    filter_backend = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=True, permission_classes=[IsAuthenticated],
            methods=['POST'])
    def favorite(self, request, pk=None):
        serial_type = FavoritesSerializer
        serializer = add_favorite_or_cart(self, request, pk, serial_type)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        model = Favorites
        delete_favorite_or_cart(self, request, pk, model)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=[IsAuthenticated],
            methods=['POST'])
    def shopping_cart(self, request, pk=None):
        serial_type = CartSerializer
        serializer = add_favorite_or_cart(self, request, pk, serial_type)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        model = Cart
        delete_favorite_or_cart(self, request, pk, model)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = IngredientsInRecipe.objects.filter(
            recipe__carts__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit').annotate(total=Sum('amount'))
        shopping_list = 'Список покупок:\n\n'
        for number, ingredient in enumerate(ingredients, start=1):
            shopping_list += (
                f'{ingredient["ingredient__name"]}: '
                f'{ingredient["total"]} '
                f'{ingredient["ingredient__measurement_unit"]}\n')

        cart = 'shopping-list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (f'attachment;'
                                           f'filename={cart}')
        return response
