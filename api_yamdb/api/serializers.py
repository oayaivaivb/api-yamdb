import string
import random

from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from reviews.models import User, Review, Comment, Category, Genre, Title


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
        error_messages={
            'invalid': 'Username содержит недопустимые символы.'
        }
    )
    email = serializers.EmailField(max_length=254)

    @staticmethod
    def generate_code():
        return ''.join(random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        ))

    def send_confirmation_email(self, user):
        send_mail(
            subject='Код подтверждения YaMDb',
            message=f'Ваш код подтверждения: {user.confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя "me" использовать запрещено.')
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        user = self.get_or_create_user(username, email)
        self.send_confirmation_email(user)
        return {'username': user.username, 'email': user.email}

    def get_or_create_user(self, username, email):
        code = self.generate_code()
        try:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'confirmation_code': code,
                }
            )
            if not created:
                if user.email != email:
                    raise serializers.ValidationError(
                        {'email': 'Email не совпадает с зарегистрированным для этого username.'}
                    )
                user.confirmation_code = code
                user.save(update_fields=['confirmation_code'])
            else:
                user.set_unusable_password()
                user.save(update_fields=['password'])
            return user
        except IntegrityError:
            raise serializers.ValidationError(
                {'email': 'Пользователь с таким email уже существует.'}
            )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=6)

    def validate(self, data):
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError(
                'Пользователь не передан в контекст.')

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
        if value == 'me':
            raise serializers.ValidationError(
                'Имя "me" использовать запрещено.')
        queryset = User.objects.filter(username=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует.')
        return value

    def validate_email(self, value):
        queryset = User.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.')
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_unusable_password()
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.IntegerField(read_only=True)
    title = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.IntegerField(read_only=True)
    review = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = '__all__'
