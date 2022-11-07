from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from recipes.views import RecipesViewSet, IngredientViewSet
from users.views import UsersViewSet

admin.site.site_header = 'Foodgram'
admin.site.index_title = 'Разделы админки Foodgram'
admin.site.site_title = 'Админка сайта Foodgram'

router = routers.DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/', include('tags.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
