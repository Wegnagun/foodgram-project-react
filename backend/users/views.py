from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser
from .pagination import CustomPagination
from .serializers import CustomUserSerializer


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
