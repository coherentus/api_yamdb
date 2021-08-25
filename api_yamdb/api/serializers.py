from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from datetime import datetime as dt

from reviews.models import Category, Comment, Genre, Review, Title, User
from users.models import User


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'rating',
                  'category', 'genre')

    def validate_year(self, value):
        year_today = dt.date.today().year
        if value > year_today:
            raise serializers.ValidationError('Проверьте год создания!')
        return value


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Недопустимое имя пользователя!')
        elif not User.objects.filter(username=value).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        return value

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = default_token_generator.make_token(user)
        if str(confirmation_code) != data['confirmation_code']:
            raise ValidationError('Неверный код подтверждения')
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('Пользователь с такой почтой '
                                  'уже зарегестрирован')
        return value

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Недопустимое имя пользователя!')
        elif User.objects.filter(username=value).exists():
            raise ValidationError('Пользователь с таким именем '
                                  'уже зарегестрирован')
        return value

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('Пользователь с такой почтой '
                                  'уже зарегестрирован')
        return value

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Недопустимое имя пользователя!')
        elif User.objects.filter(username=value).exists():
            raise ValidationError('Пользователь с таким именем '
                                  'уже зарегестрирован')
        return value

    class Meta:
        model = User
        fields = ('email', 'username')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        exclude = ('review',)
        model = Comment
