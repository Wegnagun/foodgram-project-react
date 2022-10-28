from rest_framework import serializers

from .models import Recipe


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели рецептов."""
    pass
