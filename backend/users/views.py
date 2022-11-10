from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.serializers import FollowSerializer, FollowListSerializer
from .models import User
from .pagination import CustomPagination
from .serializers import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """Контроллер пользователей."""
    pagination_class = CustomPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    search_fields = ('username',)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if request.method != 'POST':
            User.unfollow(user, author)
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = FollowSerializer(
            data={
                'user': request.user.id,
                'author': get_object_or_404(User, id=pk).id
            },
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            User.follow_for(user, author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        subscriptions_list = self.paginate_queryset(
            self.request.user.follow.all()
        )
        serializer = FollowListSerializer(
            subscriptions_list, many=True, context={
                'request': request
            }
        )
        return self.get_paginated_response(serializer.data)
