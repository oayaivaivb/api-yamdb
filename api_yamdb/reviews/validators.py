"""Модуль с валидаторами для моделей приложения reviews и API приложения."""

import datetime as dt

from django.core.exceptions import ValidationError


INVALID_USERNAME = 'me'


def validate_username_not_me(value):
    """Валидатор запрещающий использовать username 'me'."""
    if value == INVALID_USERNAME:
        raise ValidationError(
            f'Имя "{INVALID_USERNAME}" использовать запрещено.')
    return value


def validate_year(value):
    """Валидатор года выпуска произведения (не может быть в будущем)."""
    current_year = dt.date.today().year
    if value > current_year:
        raise ValidationError(
            f'Год {value} не может быть больше текущего!'
        )
