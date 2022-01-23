import django_filters as filters

from users.models import CustomUser
from .models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    author = filters.ModelChoiceFilter(
        queryset=CustomUser.objects.all()
    )
    is_favorites = filters.BooleanFilter(
        field_name='favorites',
        method='get_is_favorited',
        label='Favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='carts',
        label='Is in cart',
        method='get_is_favorited',
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorites', 'is_in_shopping_cart']

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated:
            return queryset.filter(carts__user=self.request.user)
        return queryset
