# Generated by Django 3.2.3 on 2023-05-29 07:36

import datetime
from django.db import migrations, models
import recipes.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=200, validators=[recipes.validators.measurement_unit_is_character], verbose_name='Единица измерения')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=1, verbose_name='Количество')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('text', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.IntegerField(validators=[recipes.validators.validate_cooking_time], verbose_name='Время приготовления (м)')),
                ('pub_date', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Дата публикации')),
                ('image', models.ImageField(null=True, upload_to='recipes/images/')),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, null=True, unique=True, verbose_name='Slug')),
                ('color', models.CharField(max_length=7, null=True, unique=True, verbose_name='Цвет')),
            ],
        ),
    ]
