import string
import random

from rest_framework import serializers

from .models import User


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя "me" использовать запрещено.')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.')
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_unusable_password()
        code = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        user.confirmation_code = code
        user.save()
        print(f'Код подтверждения для {user.username}: {code}')  # временно
        return user
