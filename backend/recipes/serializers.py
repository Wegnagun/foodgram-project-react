from rest_framework import serializers
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer

from .models import Recipe, Ingredient


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


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингридиентов."""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )
