from django.db.models import Q
from rest_framework import filters
from django.db.models import Q, Case, When, BooleanField

class RecipeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        is_in_shopping_cart = request.query_params.get('is_in_shopping_cart')
        tags = request.query_params.getlist('tags')
        is_favorited = request.query_params.get('is_favorited')
        author = request.query_params.get('author')

        if is_in_shopping_cart:
            queryset = queryset.filter(added_by=request.user)
        
        if author:
            queryset = queryset.filter(author=author)
        
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        
        if is_favorited:
            queryset = queryset.filter(favorited_by=request.user)
        
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

        return queryset