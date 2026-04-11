import string
import random

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from .models import User
from .validators import validate_username, validate_email


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        return validate_username(value, instance=None)

    def validate_email(self, value):
        return validate_email(value, instance=None)

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


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=6)

    def validate(self, data):
        current_username = data.get('username')
        try:
            user = User.objects.get(username=current_username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Пользователь с таким username не найден.')

        current_code = data.get('confirmation_code')
        if current_code != user.confirmation_code:
            raise serializers.ValidationError(
                'Неверный код подтверждения.')

        user.confirmation_code = ''
        user.save(update_fields=['confirmation_code'])
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        return {'access': access}


class UserSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        return validate_username(value, instance=self.instance)

    def validate_email(self, value):
        return validate_email(value, instance=self.instance)

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_unusable_password()
        user.save()
        return user

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
