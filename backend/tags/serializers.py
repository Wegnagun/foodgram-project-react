from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели тэгов."""
    model = Tag
    fields = (
        'id',
        'name',
        'color',
        'slug',
    )
