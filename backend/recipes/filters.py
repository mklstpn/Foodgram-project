from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from users.models import CustomUser
from .models import Recipe


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    author = filters.ModelChoiceFilter(
        queryset=CustomUser.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        field_name='favorites',
        method='get_is_favorited',
        label='Favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='carts',
        label='Is in cart',
        method='get_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value == 1:
                return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value == 1:
            return queryset.filter(carts__user=self.request.user)
        return queryset
