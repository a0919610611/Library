from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, generics, viewsets, status
from .serializers import *
from django.conf import settings
import requests
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
from datetime import datetime
from django.contrib.auth import authenticate

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
User = get_user_model()


class UserList(generics.ListAPIView):
    # authentication_classes = (authentication.)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'


class Register(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # try:
        user = User.objects.create_user(email=serializer.data['email'], password=serializer.data['password'])
        payload = jwt_payload_handler(user)
        print(payload)

        data = {}
        data['token'] = jwt_encode_handler(payload)
        return Response(data=data, status=status.HTTP_201_CREATED)
        # except:
        #     return Response('Some thing wrong', status=status.HTTP_200_OK)


class Login(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer

    def post(self, request):
        print('hi')
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        # try:
        email = serializer.data['email']
        password = serializer.data['password']
        print(password)
        user = authenticate(email=email, password=password)
        print(user.password)
        if user is None:
            return Response('Password Wrong', status=status.HTTP_200_OK)
        payload = jwt_payload_handler(user)
        data = {}
        data['token'] = jwt_encode_handler(payload)
        return Response(data=data, status=status.HTTP_200_OK)
        # except:
        #     return Response('Some thing wrong', status=status.HTTP_200_OK)
