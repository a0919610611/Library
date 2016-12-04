from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from api.models import *
from django.contrib.auth import get_user_model
from api.serializers import *

User = get_user_model()


# Helper Function
def create_nomaluser():
    return User.objects.create_user('test', 'test@test.com', '12345678')


def create_superuser():
    return User.objects.create_superuser('admin', 'admin@admin.com', '12345678')


# Create your tests here.

class UserTestCase(APITestCase):
    def test_list(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = reverse('user-list')
        user = dict()
        user['username'] = 'test'
        user['password'] = '12345678'
        user['first_name'] = 'test_first_name'
        user['last_name'] = 'test_last_name'
        user['email'] = 'test@test.com'
        user['address'] = 'test_address'
        user['student_id'] = '0416031'
        user['birthday'] = '2016-04-25'
        user['phone_number'] = '0919610611'
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(pk=1).username, 'test')

    def test_login_and_token(self):
        create_nomaluser()
        url = reverse('user-login')
        user = dict()
        user['username'] = 'test'
        user['password'] = '12345678'
        response = self.client.post(url, user)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict()
        data['token'] = response.data['token']
        verify_url = reverse('verify-token')
        response = self.client.post(verify_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_url = reverse('refresh-token')
        response = self.client.post(refresh_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookTestCase(APITestCase):
    def create_book(self):
        book = dict()
        book['title'] = 'title'
        book['author'] = 'author'
        book['ISBN'] = '132456778'
        book['publisher'] = 'Leo'
        book['call_number'] = '1A2B'
        barcodes = []
        barcode_1 = dict()
        barcode_1['bar_code'] = '1234'
        barcode_2 = dict()
        barcode_2['bar_code'] = '5678'
        barcodes.append(barcode_1)
        barcodes.append(barcode_2)
        book['bar_codes'] = barcodes
        serializer = BookSerializer(data=book)
        serializer.is_valid()
        data = serializer.validated_data
        return BookSerializer.create(self, data)

    def setUp(self):
        self.superuser = create_superuser()
        self.normaluser = create_nomaluser()

    def test_create(self):
        url = reverse('book-list')
        book = dict()
        book['title'] = 'title'
        book['author'] = 'author'
        book['ISBN'] = '132456778'
        book['publisher'] = 'Leo'
        book['call_number'] = '1A2B'
        barcodes = []
        barcode_1 = dict()
        barcode_1['bar_code'] = '1234'
        barcode_2 = dict()
        barcode_2['bar_code'] = '5678'
        barcodes.append(barcode_1)
        barcodes.append(barcode_2)
        book['bar_codes'] = barcodes
        self.client.force_login(user=self.normaluser)
        response = self.client.patch(url, book)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_login(user=self.superuser)
        response = self.client.post(url, book)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get()
        self.assertEqual(book.bar_codes.count(), 2)
        barcode_1 = book.bar_codes.get(id=1)
        barcode_2 = book.bar_codes.get(id=2)
        self.assertEqual(barcode_1.bar_code, '1234')
        self.assertEqual(barcode_1.book_id, book.id)
        self.assertEqual(barcode_2.bar_code, '5678')
        self.assertEqual(barcode_2.book_id, book.id)

    def test_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        old_book = self.create_book()
        url = reverse('book-detail', kwargs={'id': old_book.id})
        new_book = dict()
        new_book['title'] = 'title2'
        self.client.force_login(user=self.normaluser)
        response = self.client.patch(url, new_book)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_login(user=self.superuser)
        response = self.client.patch(url, new_book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_book = Book.objects.get(id=old_book.id)
        self.assertEqual(updated_book.title, 'title2')
