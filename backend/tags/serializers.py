from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели тэгов."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
