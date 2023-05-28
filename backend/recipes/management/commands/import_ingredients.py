import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load JSON Ingredient data'

    def add_arguments(self, parser):
        parser.add_argument('concert_file', type=str)

    def handle(self, *args, **options):
        with open(options['concert_file']) as f:
            data = json.load(f)
        for ingredient in data:
            Ingredient.objects.get_or_create(**ingredient)
        self.stdout.write(
            'Ingredients have been imported'
        )
