from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.serializers import FollowSerializer, FollowListSerializer
from .models import User, Follow
from .pagination import CustomPagination
from .serializers import (
    UserSerializer, PasswordSerializer
)


class UsersViewSet(viewsets.ModelViewSet):
    """Контроллер пользователей."""
    pagination_class = CustomPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    search_fields = ('username',)

    @action(
        detail=False, methods=['get'],
        url_path='me', permission_classes=(IsAuthenticated,)
    )
    def about_me(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path='set_password',
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        pk = self.request.user.id
        user = User.objects.get(pk=pk)
        serializer = PasswordSerializer(
            request.user, data=request.data, partial=True,
            context={"user": user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, pk):
        if request.method != 'POST':
            subscription = get_object_or_404(
                Follow,
                author=get_object_or_404(User, id=pk),
                user=request.user
            )
            self.perform_destroy(subscription)
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = FollowSerializer(
            data={
                'user': request.user.id,
                'author': get_object_or_404(User, id=pk).id
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        subscriptions_list = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = FollowListSerializer(
            subscriptions_list, many=True, context={
                'request': request
            }
        )
        return self.get_paginated_response(serializer.data)
