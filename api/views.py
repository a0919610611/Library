from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import *
from api.models import *
from rest_framework.response import Response
from rest_framework import authentication, generics, viewsets, status, decorators, permissions
from rest_framework.permissions import IsAdminUser, AllowAny
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from Library.permissions import IsOwnerOrAdmin, IsAuthenticatedOrCreate

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrCreate,)
    lookup_field = 'pk'
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(pk=self.request.user.pk)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # try:
        # username = serializer.data['username']
        # email = serializer.data['email']
        # password = serializer.data['password']
        user = User(**serializer.data)
        user.save()
        payload = jwt_payload_handler(user)
        print(payload)
        data = dict()
        data['token'] = jwt_encode_handler(payload)
        return Response(data=data, status=status.HTTP_201_CREATED)
        # except:
        #     return Response('Some thing wrong', status=status.HTTP_200_OK)

    @decorators.list_route(methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
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


class BookViewSet(viewsets.ModelViewSet):
    """
    list: show all books

    retrieve: get one book by pk
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
