from django.urls import include, path
from rest_framework import routers

from .views import UsersViewSet

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('users/set_password', UsersViewSet,
                basename='set_password')

urlpatterns = [
    path('', include(router.urls))
]