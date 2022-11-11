from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.serializers import SubscribeSerializer
from .models import User
from .pagination import CustomPagination
from .serializers import UserSerializer


class UsersViewSet(DjoserUserViewSet):
    """Контроллер пользователей."""
    pagination_class = CustomPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    additional_serializer = SubscribeSerializer
    lookup_field = 'pk'
    search_fields = ('username',)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, pk):
        author = get_object_or_404(User, id=pk)
        if request.method != 'POST':
            request.user.subscribe.remove(author)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if not author.following.filter(user=request.user).exists():
            request.user.subscribe.add(author)
            subscribe = request.user.subscribe.filter(id=pk).first()
            serializer = self.additional_serializer(
                subscribe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {'errors': 'Вы уже подписаны на данного пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        subscriptions_list = self.paginate_queryset(
            self.request.user.subscribe.all()
        )
        serializer = SubscribeSerializer(
            subscriptions_list, many=True, context={
                'request': request
            }
        )
        return self.get_paginated_response(serializer.data)
