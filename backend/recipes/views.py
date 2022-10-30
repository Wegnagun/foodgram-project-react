from rest_framework import viewsets
from .models import Recipe, Ingredient
from .serializers import RecipesSerializer, IngredientSerializer
from users.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend


class RecipesViewSet(viewsets.ModelViewSet):
    """Контроллер рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)


class IngredientViewSet(viewsets.ModelViewSet):
    """Контроллер ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('^name',)
