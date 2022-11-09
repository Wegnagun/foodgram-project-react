from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .managers import UserManager
from .validators import validate_not_me_name


class UserRole:
    USER = 'user'
    ADMIN = 'admin'
    choices = [
        (USER, 'USER'),
        (ADMIN, 'ADMIN')
    ]


class User(AbstractUser):
    """Модель пользователей."""
    username_validator = UnicodeUsernameValidator()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator, validate_not_me_name],
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
    role = models.TextField(
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name='Роль пользователя'
    )
    is_blocked = models.BooleanField('Заблокирован', default=False)
    follow = models.ManyToManyField(
        'self', through='Follow', symmetrical=False,
        through_fields=('user', 'author')
    )

    objects = UserManager()

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == UserRole.USER

    def follow_for(self, obj):
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
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='self_following',
            ),
        ]

    def __str__(self):
        return f"{self.user} follows {self.author}"
