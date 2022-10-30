from django.contrib import admin

from users.admin import BaseAdminSettings
from .models import Recipe, Ingredient


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


class IngredientAdmin(BaseAdminSettings):
    """Отображаемые поля админки раздела ингридиенты."""
    list_display = (
        'name',
        'measurement_unit'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Ingredient, IngredientAdmin)
