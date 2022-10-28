from rest_framework import serializers
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer

from .models import Recipe


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор модели рецептов."""
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', #'ingredients',
            # 'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )
