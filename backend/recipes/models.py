from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from tags.models import Tag

User = get_user_model()


class Recipe(models.Model):
    """Модель рецептов."""
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        blank=True,
        verbose_name='Фото',
        upload_to='recipes/images'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    # ingredients=models.ManyToManyField(
    #     Ingredient,
    #     through='IngredientRecipe',
    #     related_name='recipes',
    #     verbose_name='Ингредиенты в рецепте'
    # )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Не менее 1')
        ],
        verbose_name='Время приготовления, мин.'
    )
    # is_favorited = False,
    # is_in_shopping_cart = False

