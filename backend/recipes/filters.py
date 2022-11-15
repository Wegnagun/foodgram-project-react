import django_filters as filters

from .models import Recipe, Ingredient


class IngredientSearchFilter(filters.FilterSet):
    """Фильтр поиска по названию ингредиента."""
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(filters.FilterSet):
    """ Фильтр для рецептов и тегов. """
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.CharFilter(
        field_name='is_favorited', method='get_is_favorited'
    )
    is_in_shopping_cart = filters.CharFilter(
        field_name='is_in_shopping_cart', method='get_is_in_shopping_cart'
    )
    author = filters.AllValuesMultipleFilter(field_name='author__id')

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def get_is_favorited(self, queryset, name, value):
        if value in [True, '1']:
            return queryset.filter(favoriting__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value in [True, '1']:
            return queryset.filter(purchases__user=self.request.user)
        return queryset
