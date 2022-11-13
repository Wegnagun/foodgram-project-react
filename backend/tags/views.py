from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from .models import Tag
from .serializers import TagSerializer
from recipes.filters import RecipeFilter


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """ Контроллер тэгов. """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None
    filter_class = RecipeFilter
