from rest_framework import serializers

from .models import User


def validate_username(value, instance=None):
    if value == 'me':
        raise serializers.ValidationError(
            'Имя "me" использовать запрещено.')
    qs = User.objects.filter(username=value)
    if instance:
        qs = qs.exclude(pk=instance.pk)
    if qs.exists():
        raise serializers.ValidationError(
            'Пользователь с таким username уже существует.')
    return value


def validate_email(value, instance=None):
    qs = User.objects.filter(email=value)
    if instance:
        qs = qs.exclude(pk=instance.pk)
    if qs.exists():
        raise serializers.ValidationError(
            'Пользователь с таким email уже существует.')
    return value
