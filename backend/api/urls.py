from django.urls import include, path
from rest_framework import routers

from users.views import UsersViewSet, UserDetailViewSet

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register(r'users/(?P<user_id>\d+)/', UserDetailViewSet,
                basename='user_detail')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
