from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from users.pagination import CustomPagination
from .models import Recipe, Ingredient, Purchase
from .serializers import (
    RecipesSerializer, IngredientSerializer, RecipeCreateSerializer,
    PurchaseSerializer
)


class RecipesViewSet(viewsets.ModelViewSet):
    """Контроллер рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipesSerializer
        return RecipeCreateSerializer

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_instance = get_object_or_404(model, user=user, recipe=recipe)
        model_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk):
        return self.post_method_for_actions(
            request, pk, serializers=PurchaseSerializer
        )

    @purchase.mapping.delete
    def delete_purchase(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Purchase)


class IngredientViewSet(viewsets.ModelViewSet):
    """Контроллер ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('^name',)
