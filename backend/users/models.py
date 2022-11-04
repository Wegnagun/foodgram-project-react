from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from .managers import CustomUserManager
# from recipes.models import IngredientInRecipe


class CustomUser(AbstractUser, PermissionsMixin):
    """Модель пользователей."""
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        verbose_name='Имя пользователя',
        help_text=(
            "Обязательно. 150 символов или меньше. "
            "Буквы, цифры and @/./+/-/_ только."
        ),
        error_messages={
            "unique": "Пользователь с таким username уже есть.",
        },
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
        error_messages={
            "unique": "Пользователь с таким email уже есть.",
        },
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )
    is_superuser = models.BooleanField('Администратор', default=False)
    is_blocked = models.BooleanField('Заблокирован', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    objects = CustomUserManager()

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_staff(self):
        return self.is_superuser

    def is_following(self, obj):
        return Follow.objects.filter(
            user=self,
            author=obj
        ).exists()

    def follow(self, obj):
        Follow.objects.get_or_create(
            user=self,
            author=obj
        )

    def unfollow(self, obj):
        Follow.objects.filter(
            user=self,
            author=obj
        ).delete()

    # def clear_shopping_cart(self):
    #     self.purchases.all().delete()
    #
    # def get_shopping_cart(self):
    #     purchases = self.purchases
    #     if not purchases.exists():
    #         return None
    #     user_recipes_for_shopping = [
    #         purchase.recipe.name for purchase in purchases.all()
    #     ]
    #     shopping_cart = IngredientInRecipe.objects.filter(
    #         recipe__purchases__user=self
    #     ).values(
    #         ingredient_name=models.F('ingredient__name'),
    #         ingredient_measurement_unit=
    #         models.F('ingredient__measurement_unit'),
    #     ).annotate(
    #         ingredient_amount=models.Sum('amount'),
    #     ).order_by('ingredient_name')
    #
    #     return {
    #         'recipes_in_cart': user_recipes_for_shopping,
    #         'purchases': shopping_cart
    #     }

    def __str__(self):
        return self.username


class Follow(models.Model):
    """ Модель подписок. """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь - кто подписан",
        related_name="follower"
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь - на кого подписан",
        related_name="following"
    )

    class Meta:
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "user"],
                name="Follow_unique"
            ),
        ]

    def __str__(self):
        return f"{self.user} follows {self.author}"
