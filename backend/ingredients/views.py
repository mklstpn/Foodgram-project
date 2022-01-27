from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from recipes.filters import IngredientSearchFilter
from .models import Ingredient
from .serializers import Ingredientserializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = Ingredientserializer
    paginator = None
    permission_classes = (AllowAny, )
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)
