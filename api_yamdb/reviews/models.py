from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_year


ROLE_CHOICES = [
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Роль'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Биография'
    )
    confirmation_code = models.CharField(
        max_length=6,
        blank=True,
        verbose_name='Код подтверждения'
    )

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.IntegerField(validators=[validate_year],
                               verbose_name='Год выпуска')
    description = models.TextField(blank=True, verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
