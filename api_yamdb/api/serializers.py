from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from users.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status


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
