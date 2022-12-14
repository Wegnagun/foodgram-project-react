from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from tags.serializers import TagSerializer
from users.models import User
from users.serializers import UserSerializer
from .models import (
    Recipe, Ingredient, IngredientInRecipe, Favorite, Purchase, Tag
)


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор модели ингредиентов. """
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор ингредиентов в рецепте. """
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='measurement_unit',
        read_only=True,
    )
    name = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipesSerializer(serializers.ModelSerializer):
    """ Сериализатор модели рецептов. """
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    @staticmethod
    def get_ingredients(obj):
        ingredients = IngredientInRecipe.objects.filter(recipe_parent=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return request.user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return request.user.purchases.filter(recipe=obj).exists()


class AddIngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор добавления ингредиентов. """
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')

    def validate_amount(self, data):
        if int(data) < 1:
            raise serializers.ValidationError({
                'ingredients': (
                    'Количество должно быть больше 1'
                ),
                'msg': data
            })
        return data

    def create(self, validated_data):
        return IngredientInRecipe.objects.create(
            ingredient=validated_data.get('id'),
            amount=validated_data.get('amount')
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор создания рецепта. """
    image = Base64ImageField(use_url=True, max_length=None)
    author = UserSerializer(read_only=True)
    ingredients = AddIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'image', 'tags', 'author', 'ingredients',
            'name', 'text', 'cooking_time',
        )

    def create_ingredients(self, recipe, ingredients):
        IngredientInRecipe.objects.bulk_create([
            IngredientInRecipe(
                recipe_parent=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['ingredient'],
            ) for ingredient in ingredients
        ])

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError(
                    'Есть повторяющиеся ингредиенты!'
                )
            ingredients_list.append(ingredient_id)
        if data['cooking_time'] <= 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше 0!'
            )
        return data

    @atomic
    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=request.user,
            **validated_data
        )
        self.create_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    @atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = instance
        IngredientInRecipe.objects.filter(recipe_parent=recipe).delete()
        self.create_ingredients(recipe, ingredients)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        return RecipesSerializer(
            instance,
            context={
                'request': self.context.get('request'),
            }
        ).data


class RecipeShortInfoSerializer(serializers.ModelSerializer):
    """ Краткая инфа о рецепте. """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class PurchaseSerializer(serializers.ModelSerializer):
    """ Сериализатор списка покупок. """
    class Meta:
        model = Purchase
        fields = ['recipe', 'user']

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        purchase_exists = Purchase.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()

        if request.method == 'POST' and purchase_exists:
            raise serializers.ValidationError(
                'Рецепт уже в списке покупок'
            )

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortInfoSerializer(
            instance.recipe,
            context=context).data


class FavoriteSerializer(serializers.ModelSerializer):
    """ Сериализатор избранного. """
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Уже есть в избранном.'
            })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortInfoSerializer(
            instance.recipe, context=context).data


class SubscribeSerializer(UserSerializer):
    """ Сериализатор подписок. """
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + (
            'recipes', 'recipes_count', 'is_subscribed'
        )

    def get_recipes_count(self, author):
        return Recipe.objects.filter(author=author).count()

    def get_recipes(self, author):
        queryset = self.context.get('request')
        recipes_limit = queryset.query_params.get('recipes_limit')
        if not recipes_limit:
            return RecipeShortInfoSerializer(
                Recipe.objects.filter(author=author),
                many=True, context={'request': queryset}
            ).data
        return RecipeShortInfoSerializer(
            Recipe.objects.filter(author=author)[:int(recipes_limit)],
            many=True,
            context={'request': queryset}
        ).data
