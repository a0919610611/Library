from rest_framework import serializers
from api.models import *
from django.contrib.auth import get_user_model


class BarCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarCode
        fields = ('id', 'bar_code', 'is_borrowed', 'book')
        # depth = 1


class BookSerializer(serializers.ModelSerializer):
    bar_codes = BarCodeSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'ISBN', 'publisher', 'call_number', 'bar_codes')
        extra_kwargs = {
        }

    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        if 'bar_codes' in validated_data:
            bar_codes_data = validated_data.pop('bar_codes')
            for barcode in bar_codes_data:
                bc = BarCode(**barcode)
                bc.book = book
                bc.save()
                book.save()
        return book

    def update(self, instance, validated_data):
        try:
            bar_codes_data = validated_data.pop('bar_codes')
        except:
            bar_codes_data = {}
        for key, value in validated_data.items():
            setattr(instance, key, value)
        bar_codes = [item['bar_code'] for item in bar_codes_data]
        instance_barcodes = []
        for barcode in instance.bar_codes.all():
            instance_barcodes.append(barcode.bar_code)
            if barcode.bar_code not in bar_codes:
                barcode.delete()
        for barcode in bar_codes_data:
            if barcode['bar_code'] in instance_barcodes:
                continue
            bc = BarCode(**barcode)
            bc.book = instance
            bc.save()
        instance.save()
        return instance


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'student_id', 'address', 'birthday', 'first_name', 'last_name', 'phone_number'
            , 'is_staff', 'date_joined', 'password')
        read_only_fields = ('is_staff', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True, 'allow_null': True},
        }


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'student_id', 'address', 'birthday', 'first_name', 'last_name', 'phone_number'
            , 'is_staff', 'date_joined', 'password', 'is_staff')
        read_only_fields = ('date_joined',)
        extra_kwargs = {
            'password': {'write_only': True, 'allow_null': True},
        }
