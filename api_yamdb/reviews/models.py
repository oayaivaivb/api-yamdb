"""Модуль моделей приложения reviews."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_year


ROLE_CHOICES = [
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class User(AbstractUser):
    """Модель пользователя с расширенными правами."""

    email = models.EmailField(
        'Email',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
    )
    bio = models.TextField(
        'Биография',
        max_length=500,
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=6,
        blank=True,
    )

    def is_admin(self):
        """Проверка, является ли пользователь администратором."""
        return self.role == 'admin' or self.is_superuser

    def is_moderator(self):
        """Проверка, является ли пользователь модератором."""
        return self.role == 'moderator'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField(
        'Название',
        max_length=256,
    )
    slug = models.SlugField(
        'Слаг',
        unique=True, 
        max_length=50
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Строковое представление категории."""
        return self.name


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField(
        'Название',
        max_length=256,
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        """Строковое представление жанра."""
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        'Название',
        max_length=256
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=[validate_year]
    )
    description = models.TextField(
        'Описание',
        blank=True
    )
    genre = models.ManyToManyField(
        'Жанр',
        Genre,
        related_name='titles',
    )
    category = models.ForeignKey(
        'Категория',
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        """Строковое представление произведения."""
        return self.name


class Review(models.Model):
    """Модель отзыва на произведение."""

    title = models.ForeignKey(
        'Произведение',
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    author = models.ForeignKey(
        'Автор',
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField('Текст отзыва')
    score = models.IntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    """Модель комментария к отзыву."""

    review = models.ForeignKey(
        'Отзыв',
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        'Автор',
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
