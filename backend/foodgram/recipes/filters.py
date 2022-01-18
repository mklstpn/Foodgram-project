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

    class Meta:
        model = Recipe
        fields = ['tags', 'author']
