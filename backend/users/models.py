from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .managers import UserManager


class User(AbstractUser):
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
    objects = UserManager()

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

    def __str__(self):
        return self.username


class Follow(models.Model):
    """ Модель подписок. """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь - кто подписан",
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
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
