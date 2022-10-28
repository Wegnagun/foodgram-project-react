from rest_framework import viewsets
from .models import Recipe
from .serializers import RecipesSerializer
from users.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend


class RecipesViewSet(viewsets.ModelViewSet):
    """Контроллер рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
