"""Модуль моделей приложения reviews."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)


from .validators import validate_year, validate_username_not_me
from .constants import (
    USER, MODERATOR, ADMIN,
    ROLE_CHOICES, MAX_ROLE_LEN,
    MAX_USERNAME_LEN, MAX_EMAIL_LEN, MAX_BIO_LEN, MAX_CONFIRMATION_CODE_LEN,
    MAX_NAME_LEN, MAX_SLUG_LEN
)


class User(AbstractUser):
    """Модель пользователя с расширенными правами."""
    username = models.CharField(
        max_length=MAX_USERNAME_LEN,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Username содержит недопустимые символы.'
            ),
            validate_username_not_me,
        ],
        error_messages={
            'unique': 'Пользователь с таким username уже существует.'
        }
    )

    email = models.EmailField(
        'Email',
        max_length=MAX_EMAIL_LEN,
        unique=True,
    )
    role = models.CharField(
        'Роль',
        max_length=MAX_ROLE_LEN,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        'Биография',
        max_length=MAX_BIO_LEN,
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=MAX_CONFIRMATION_CODE_LEN,
        blank=True,
    )

    def is_admin(self):
        """Проверка, является ли пользователь администратором."""
        return self.role == ADMIN or self.is_superuser

    def is_moderator(self):
        """Проверка, является ли пользователь модератором."""
        return self.role == MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']


class BaseCategoryGenreModel(models.Model):
    """Абстрактная модель для категорий и жанров."""
    name = models.CharField(
        'Название',
        max_length=MAX_NAME_LEN,
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
        max_length=MAX_SLUG_LEN,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(BaseCategoryGenreModel):
    """Модель категории произведения."""

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseCategoryGenreModel):
    """Модель жанра произведения."""

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        'Название',
        max_length=MAX_NAME_LEN
    )
    year = models.SmallIntegerField(
        'Год выпуска',
        validators=[validate_year]
    )
    description = models.TextField(
        'Описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        """Строковое представление произведения."""
        return self.name


class BaseContent(models.Model):
    """Абстрактная модель для отзывов и комментариев."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']


class Review(BaseContent):
    """Модель отзыва на произведение."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta(BaseContent.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(BaseContent):
    """Модель комментария к отзыву."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )

    class Meta(BaseContent.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
