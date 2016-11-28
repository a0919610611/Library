from rest_framework import serializers
from api.models import *
from django.contrib.auth import get_user_model


# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         models = Author
#         fields = ('name',)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'ISBN', 'total_number')
        extra_kwargs = {
        }
