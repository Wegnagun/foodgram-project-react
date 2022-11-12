from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from tags.models import Tag
from users.models import User


class Ingredient(models.Model):
    """ Модель ингредиентов. """
    name = models.CharField(
        max_length=250,
        unique=True,
        verbose_name='Наименование ингредиента',
        db_index=True,
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


class IngredientInRecipe(models.Model):
    """ Модель ингредиентов в рецепте. """
    recipe_parent = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='+'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Название ингредиента в рецепте',
        related_name='+'
    )
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
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe_parent'],
                name='recipe_ingredient_unique',
            )
        ]

    def __str__(self) -> str:
        return (
            f"{self.ingredient} в рецепте {self.recipe_parent} - "
            f"{self.amount} {self.ingredient.measurement_unit}"
        )


class Recipe(models.Model):
    """ Модель рецептов. """
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
        symmetrical=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name="recipes"
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    ingredients = models.ManyToManyField(
        IngredientInRecipe,
        symmetrical=False
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


class Favorite(models.Model):
    """ Модель избранного. """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
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
    """ Модель списка покупок. """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='purchase_user_recipe_unique'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок {self.user}'
