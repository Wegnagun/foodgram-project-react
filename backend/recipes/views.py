from django.db.models import Sum, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from users.pagination import CustomPagination
from .filters import RecipeFilter
from .models import Recipe, Ingredient, Purchase, IngredientInRecipe, Favorite
from .serializers import (
    RecipesSerializer, IngredientSerializer, RecipeCreateSerializer,
    PurchaseSerializer, FavoriteSerializer
)


class RecipesViewSet(viewsets.ModelViewSet):
    """Контроллер рецептов."""
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

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
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request, pk, serializers=PurchaseSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Purchase)

    @action(
        detail=False,
        methods=('get',),
        url_path='download_shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        purchase_list = IngredientInRecipe.objects.filter(
            recipe__purchases__user=request.user
        ).values(
            name=F('ingredient__name'),
            measurement_unit=F('ingredient__measurement_unit')
        ).annotate(amount=Sum('amount')).values_list(
            'ingredient__name', 'amount', 'ingredient__measurement_unit'
        )
        text = 'Cписок покупок:  \n '
        for ingredients in purchase_list:
            name, measurement_unit, amount = ingredients
            text += f' {name} :  {amount}   {measurement_unit} \n '
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="purchase_list.pdf"'
        )
        return response

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite)


class IngredientViewSet(viewsets.ModelViewSet):
    """Контроллер ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('^name',)
    pagination_class = None
