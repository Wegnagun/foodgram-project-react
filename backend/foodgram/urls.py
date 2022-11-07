from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from recipes.views import RecipesViewSet, IngredientViewSet
from users.views import UsersViewSet
from tags.views import TagViewSet

admin.site.site_header = 'Foodgram'
admin.site.index_title = 'Разделы админки Foodgram'
admin.site.site_title = 'Админка сайта Foodgram'

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
]
