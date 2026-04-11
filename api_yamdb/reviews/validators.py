"""Модуль с валидаторами для моделей приложения reviews."""

import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    """Валидатор года выпуска произведения (не может быть в будущем)."""
    current_year = dt.date.today().year
    if value > current_year:
        raise ValidationError(
            f'Год {value} не может быть больше текущего!'
        )
