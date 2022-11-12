from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from users.models import Follow
from .models import Recipe, Ingredient, IngredientInRecipe, Purchase, Favorite


class TabularRecipeIngredientAdmin(admin.TabularInline):
    model = IngredientInRecipe
    fk_name = 'recipe_parent'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('^name',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    model = IngredientInRecipe
    fk_name = 'recipe'


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorited')
    list_filter = ('author', 'name', 'tags')
    exclude = ('ingredients',)
    search_fields = ('^name',)
    filter_horizontal = ('tags',)
    inlines = [
        TabularRecipeIngredientAdmin,
    ]

    @admin.display(empty_value='Никто')
    def favorited(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    favorited.short_description = 'Кол-во людей добавивших в избранное'


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Follow)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
