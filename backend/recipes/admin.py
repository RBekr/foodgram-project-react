from django.conf import settings
from django.contrib import admin

from .models import Ingredient, IngredientRecipe, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    list_filter = ('author', 'name', 'tags')
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    list_filter = ('recipe', 'ingredient',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    list_filter = ('name',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY
