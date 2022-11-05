from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from tags.models import Tag
from users.models import CustomUser

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Наименование ингредиента',
        db_index=True,
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


def get_sentinel_user():
    return User.objects.get_or_create(
        username='deleted_usr',
        first_name='deleted',
        last_name='user'
    )[0]


class Recipe(models.Model):
    """Модель рецептов."""
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        unique=True,
        error_messages={
            'unique': "Рецепт с таким названием уже создан."
        },
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
        verbose_name='Тэги',
        related_name="recipes",
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET(get_sentinel_user),
        verbose_name='Автор рецепта',
        related_name="recipes"
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Время приготовления не может быть меньше 1 мин.'
            ),
            MaxValueValidator(
                32767,
                message='Время приготовления не может быть больше 32767 мин.'
            ),
        ],
        verbose_name='Время приготовления, мин.',
        help_text=(
            "Не может быть меньше минуты!"
        ),
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """Модель ингредиентов в рецепте."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Название ингредиента в рецепте')
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента в рецепте',
        validators=[
            MinValueValidator(
                1,
                message='Количество ингредиентов не может быть меньше 1.'
            ),
            MaxValueValidator(
                32767,
                message='Количество ингредиентов не может быть больше 32767.'
            )
        ]
    )

    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = 'Количество ингредиентов в рецептах'
        default_related_name = 'ingredients_recipe'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='recipe_ingredient_unique',
            )
        ]

    def __str__(self) -> str:
        return (
            f"{self.ingredient} в рецепте {self.recipe} - {self.amount} "
            f"{self.ingredient.measurement_unit}"
        )


class Favorite(models.Model):
    """ Модель избранного. """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        ordering = ('-date_added',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='favorite_user_recept_unique'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.user}'


class Purchase(models.Model):
    """ Модель покупок. """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='purchases',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchases',
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        ordering = ('-date_added',)
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='purchase_user_recipe_unique'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок {self.user}'
