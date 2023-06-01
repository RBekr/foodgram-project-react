from datetime import datetime

from colorfield.fields import ColorField
from django.db import models

from users.models import User

from .validators import measurement_unit_is_character, validate_cooking_time


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=200,
        unique=True,
        null=True
    )

    color = ColorField(
        default='#FF0000',
        verbose_name='Цвет',
        max_length=7,
        null=True,
        unique=True,
    )

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
        validators=(measurement_unit_is_character, )
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (м)',
        validators=(validate_cooking_time, )
    )
    pub_date = models.DateTimeField(
        'Дата публикации', default=datetime.now, blank=True
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
    )
    favorited_by = models.ManyToManyField(
        User,
        related_name='favorite_recipes',
        blank=True
    )
    added_by = models.ManyToManyField(
        User,
        related_name='shopping_cart',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.recipe} {self.ingredient} {self.amount}'
