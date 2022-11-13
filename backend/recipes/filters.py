import django_filters as filters

from tags.models import Tag
from .models import Recipe, User


class RecipeFilter(filters.FilterSet):
    tags = filters.tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug'
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    is_favorited = filters.NumberFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(purchases__user=self.request.user)
        return queryset
