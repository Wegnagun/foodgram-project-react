from django.urls import include, path
from rest_framework import routers

from .views import RecipesViewSet, IngredientViewSet

router = routers.DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]