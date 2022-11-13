from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from recipes.views import RecipesViewSet, IngredientViewSet
from tags.views import TagViewSet

admin.site.site_header = 'Foodgram'
admin.site.index_title = 'Разделы админки Foodgram'
admin.site.site_title = 'Админка сайта Foodgram'

router = routers.DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('djoser.urls')),
    path('api/', include(router.urls)),
]
