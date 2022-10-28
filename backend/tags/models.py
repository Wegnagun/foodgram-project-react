from django.db import models
from colorfield.fields import ColorField
from django.core.validators import validate_slug


class Tag(models.Model):
    """Модель Тэгов."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега',
        db_index=True,
        help_text=(
            "Обязательно. 200 символов или меньше."
        ),
    )
    color = ColorField(
        format='hex',
        verbose_name='HEX-код цвета'
    ),
    slug = models.SlugField(
        max_length=200,
        verbose_name='Slug',
        unique=True,
        validators=[validate_slug],
        help_text=(
            "Обязательно. 200 символов или меньше. "
            "Буквы, цифры and [a-zA-Z0-9] только."
        ),
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.slug
