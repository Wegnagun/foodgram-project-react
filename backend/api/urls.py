from django.urls import include, path
from rest_framework import routers

from users.views import UsersViewSet

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('users/set_password', UsersViewSet,
                basename='set_password')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('tags.urls')),
    path('', include('recipes.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
