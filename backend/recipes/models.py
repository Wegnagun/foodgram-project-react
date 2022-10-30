from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from tags.models import Tag

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Наименование ингредиента',
        db_index=True,
        unique=True,
        error_messages={
            "unique": "Такой ингридиент уже есть.",
        },
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}/{self.measurement_unit}'


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
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        # through='IngredientRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты в рецепте'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Не менее 1')
        ],
        verbose_name='Время приготовления, мин.',
        help_text=(
            "Не может быть меньше минуты!"
        ),
    )
    # is_favorited = False,
    # is_in_shopping_cart = False

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
