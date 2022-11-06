import json

from django.core.management.base import BaseCommand
from recipes.models import Ingredient
from tags.models import Tag

TABLES = [
    (Ingredient, 'ingredients.json'),
    (Tag, 'tags.json')
]


class Command(BaseCommand):
    help = 'загрузка данныз из json в базу'

    def handle(self, *args, **options):
        options_list = (options['t'], options['i'])
        if any(map(None.__ne__, options_list)):
            for elem in set(options_list):
                if elem is not None:
                    try:
                        file = open(f'../data/{elem}',
                                    'r', encoding='utf-8')
                    except IOError:
                        self.stdout.write(self.style.ERROR(
                            'Не удалось открыть файл!'))
                    else:
                        model = next(filter(lambda x: x[1] == elem, TABLES),
                                     None)
                        with file:
                            reader = json.load(file)
                            model[0].objects.bulk_create(
                                model[0](**data) for data in reader)
                        self.stdout.write(self.style.SUCCESS(
                            f'Модель {str(model[0])} обновлена!'))

        else:
            for model, data in TABLES:
                try:
                    file = open(f'../data/{data}', 'r',
                                encoding='utf-8')
                except IOError:
                    self.stdout.write(self.style.ERROR(
                        'Не удалось открыть файл!'))
                else:
                    with file:
                        reader = json.load(file)
                        model.objects.bulk_create(
                            model(**data) for data in reader)
                        self.stdout.write(self.style.SUCCESS(
                            f'Модель {str(model[0])} обновлена!'))

    def add_arguments(self, parser):
        parser.add_argument(
            '-t',
            const='tags.json',
            nargs='?',
            type=str,
            help='Загрузить tags.json в базу'
        )
        parser.add_argument(
            '-i',
            const='ingredients.json',
            nargs='?',
            type=str,
            help='Загрузить ingredients.json в базу'
        )
