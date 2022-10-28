from django.urls import include, path
from rest_framework import routers

from .views import RecipesViewSet

router = routers.DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]