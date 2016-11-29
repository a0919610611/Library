from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, generics, viewsets, status
from rest_framework.permissions import IsAdminUser
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
from datetime import datetime
from django.contrib.auth import authenticate
from Library.permissions import IsOwnerOrAdmin

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsOwnerOrAdmin,)
    serializer_class = UserSerializer
    lookup_field = 'pk'
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(pk=self.request.user.pk)


class Register(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # try:
        username = serializer.data['username']
        email = serializer.data['email']
        password = serializer.data['password']
        user = User.objects.create_user(username=username, email=email,
                                        password=password)
        payload = jwt_payload_handler(user)
        print(payload)
        data = {}
        data['token'] = jwt_encode_handler(payload)
        return Response(data=data, status=status.HTTP_201_CREATED)
        # except:
        #     return Response('Some thing wrong', status=status.HTTP_200_OK)


class Login(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        # try:
        username = serializer.data['username']
        password = serializer.data['password']
        data = {}
        try:
            user = User.objects.get(username=username)
        except:
            data['error'] = 'No This User'
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        user = authenticate(username=username, password=password)
        if user is None:
            data['error'] = 'Password Wrong'
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        payload = jwt_payload_handler(user)
        data = dict()
        data['token'] = jwt_encode_handler(payload)
        return Response(data=data, status=status.HTTP_200_OK)
