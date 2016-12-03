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

    def test_login(self):
        self.test_create()
        url = reverse('user-login')
        user = dict()
        user['username'] = 'test'
        user['password'] = '12345678'
        response = self.client.post(url, user)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookTestCase(APITestCase):
    def test_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
