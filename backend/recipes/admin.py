from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from users.admin import BaseAdminSettings
from users.models import Follow
from .models import Recipe, Ingredient, IngredientInRecipe, Purchase, Favorite


class RecipeIngredientAdmin(admin.TabularInline):
    model = IngredientInRecipe
    fk_name = 'recipe'


class RecipesAdmin(BaseAdminSettings):
    """Отображаемые поля админки раздела рецепты."""
    list_display = (
        'name',
        'author',
    )
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags', 'ingredients')
    list_display_links = ('name',)
    filter_horizontal = ('tags', 'ingredients')
    inlines = [
        RecipeIngredientAdmin,
    ]


class IngredientAdmin(BaseAdminSettings):
    """Отображаемые поля админки раздела ингридиенты."""
    list_display = (
        'name',
        'measurement_unit'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')


admin.site.register(Follow, SubscriptionAdmin)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientInRecipe, RecipeIngredientAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Favorite, FavoriteAdmin)
