from django.urls import include, path
from rest_framework import routers

from .views import UsersViewSet

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
