from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from api.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


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
        self.test_create()
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
    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', '12345678')

    def test_create(self):
        url = reverse('book-list')
        book = dict()
        book['title'] = 'title'
        book['author'] = 'author'
        book['ISBN'] = '132456778'
        book['publisher'] = 'Leo'
        book['call_number'] = '1A2B'
        self.client.force_login(user=self.user)
        response = self.client.post(url, book)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
