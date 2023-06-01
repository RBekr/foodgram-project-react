from django.db.models import BooleanField, Case, Q, When
from django_filters.rest_framework import filters, FilterSet

from recipes.models import Ingredient, Recipe, Tag

class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorited_by=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(added_by=self.request.user)
        return queryset


class IngredientFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search_params = request.query_params.get('name', None)

        if search_params:
            startswith_query = Q(name__istartswith=search_params)
            contains_query = Q(name__icontains=search_params)

            queryset = queryset.annotate(
                starts_with_match=Case(
                    When(startswith_query, then=True),
                    default=False,
                    output_field=BooleanField()
                ),
                contains_match=Case(
                    When(contains_query & ~startswith_query, then=True),
                    default=False,
                    output_field=BooleanField()
                )
            ).filter(startswith_query | contains_query).order_by(
                '-starts_with_match',
                '-contains_match',
                'name'
            )

        return queryset  # noqa: R504
