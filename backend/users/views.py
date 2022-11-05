from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser
from .pagination import CustomPagination
from .serializers import (
    CustomUserSerializer, PasswordSerializer
)


class UsersViewSet(viewsets.ModelViewSet):
    """Контроллер пользователей."""
    pagination_class = CustomPagination
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'pk'
    search_fields = ('username',)

    @action(
        detail=False, methods=['get'],
        url_path='me', permission_classes=(IsAuthenticated,)
    )
    def about_me(self, request):
        serializer = CustomUserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path='set_password',
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        pk = self.request.user.id
        user = CustomUser.objects.get(pk=pk)
        serializer = PasswordSerializer(
            request.user, data=request.data, partial=True,
            context={"user": user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
