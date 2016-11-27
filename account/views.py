from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, generics, viewsets, status
from .serializers import *
from django.conf import settings
import requests
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
from datetime import datetime

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
User = get_user_model()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'


class Register(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            user = User.objects.create_user(email=request.data['email'], password=request.data['password'])
            return Response('Good', status=status.HTTP_201_CREATED)
        except:
            return Response('Some thing wrong', status=status.HTTP_200_OK)


'''
class Login(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, email, password):
'''
