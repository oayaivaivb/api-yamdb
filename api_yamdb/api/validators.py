"""Модуль валидаторов для API приложения."""

from django.core.exceptions import ValidationError


INVALID_USERNAME = 'me'


def validate_username_not_me(value):
    """Валидатор запрещающий использовать username 'me'."""
    if value == INVALID_USERNAME:
        raise ValidationError(
            f'Имя "{INVALID_USERNAME}" использовать запрещено.')
    return value
