import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title


class Command(BaseCommand):
    help = 'Импорт данных из CSV файлов'

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'static/data/')

        with open(os.path.join(path, 'category.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write(self.style.SUCCESS('Категории загружены'))

        with open(os.path.join(path, 'genre.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write(self.style.SUCCESS('Жанры загружены'))

        with open(os.path.join(path, 'titles.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                category = Category.objects.get(id=row['category'])
                Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=category
                )
        self.stdout.write(self.style.SUCCESS('Произведения загружены'))

        with open(os.path.join(path,
                               'genre_title.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)
        self.stdout.write(self.style.SUCCESS('Связи жанров добавлены'))

        self.stdout.write(self.style.SUCCESS('--- ИМПОРТ ЗАВЕРШЕН ---'))
