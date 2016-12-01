from rest_framework import serializers
from api.models import *
from django.contrib.auth import get_user_model


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'ISBN')
        extra_kwargs = {
        }


User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password',)
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'birthday', 'first_name', 'last_name', 'phone_number'
                  , 'is_staff', 'date_joined', 'password')
        read_only_fields = ('is_staff', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True},
        }
