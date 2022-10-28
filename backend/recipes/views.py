from rest_framework import viewsets
from .models import Recipe
from .serializers import TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Контроллер рецептов."""
    pass
