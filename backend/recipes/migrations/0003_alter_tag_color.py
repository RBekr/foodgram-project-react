# Generated by Django 3.2.3 on 2023-05-29 08:11

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default='#FF0000', image_field=None, max_length=7, null=True, samples=None, unique=True, verbose_name='Цвет'),
        ),
    ]