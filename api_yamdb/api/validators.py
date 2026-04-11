"""Модуль валидаторов для API приложения."""

from django.core.exceptions import ValidationError


def validate_username_not_me(value):
    """Валидатор запрещающий использовать username 'me'."""
    if value == 'me':
        raise ValidationError('Имя "me" использовать запрещено.')
