from rest_framework import viewsets

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    """Контроллер тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ('get',)
