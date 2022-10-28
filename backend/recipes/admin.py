from django.contrib import admin

from users.admin import BaseAdminSettings
from .models import Recipe


class RecipesAdmin(BaseAdminSettings):
    """Отображаемые поля админки раздела рецепты."""
    list_display = (
        'name',
        'author',
        # 'in_favorite'
    )
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    list_display_links = ('name',)
    # readonly_fields = ('in_favorite',)
    filter_horizontal = ('tags',)


admin.site.register(Recipe, RecipesAdmin)
