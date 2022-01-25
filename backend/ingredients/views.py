from rest_framework import viewsets

from .models import Ingredient
from .serializers import Ingredientserializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = Ingredientserializer
    paginator = None
