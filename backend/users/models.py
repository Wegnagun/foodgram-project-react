from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from .managers import CustomUserManager


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
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    is_superuser = models.BooleanField('Администратор', default=False)
    is_blocked = models.BooleanField('Заблокирован', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser
