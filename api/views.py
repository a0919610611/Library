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
from drf_haystack.serializers import HaystackSerializer
from drf_haystack.viewsets import HaystackViewSet
from api.search_indexes import *

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
User = get_user_model()


class BookSearchSerializer(HaystackSerializer):
    class Meta:
        index_classes = [BookIndex, ]
        fields = ['title', 'author', 'ISBN', ]


class BookSearchViewSet(HaystackViewSet):
    index_models = [Book, ]
    serializer_class = BookSearchSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    create: Create New User And Get Token
    login: Username And Password To ExChange Token
    """
    lookup_field = 'username'

    def get_permissions(self):
        if self.action in ('login', 'create'):
            self.permission_classes = [AllowAny, ]
        elif self.action in ('destroy',):
            self.permission_classes = [IsAdminUser, ]
        return super(self.__class__, self).get_permissions()

    def get_serializer_class(self):
        print(self.action)
        serializer = UserSerializer
        if self.action == 'login':
            serializer = LoginSerializer
        elif self.request.user.is_superuser:
            serializer = AdminUserSerializer
        elif self.action in ('partially_update', 'update'):
            serializer = UserPatchSerializer
        return serializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(pk=self.request.user.pk)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        data = dict()
        if serializer.errors:

            data['errors'] = serializer.errors
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        user = User(**serializer.validated_data)
        user.set_password(serializer.validated_data['password'])
        user.save()
        payload = jwt_payload_handler(user)

        data['token'] = jwt_encode_handler(payload)
        return Response(data=data, status=status.HTTP_201_CREATED)

    @decorators.list_route(methods=['post'], url_path='login')
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        data = {}
        try:
            user = User.objects.get(username=username)
        except:
            data['errors'] = 'No This User'
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is None:
            data['errors'] = 'Password Wrong'
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt_payload_handler(user)
        data = dict()
        data['token'] = jwt_encode_handler(payload)
        return Response(data=data, status=status.HTTP_200_OK)


class BookViewSet(viewsets.ModelViewSet):
    """
    list: show all books

    retrieve: get one book by pk
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class BarCodeViewSet(viewsets.ModelViewSet):
    queryset = BarCode.objects.all()
    serializer_class = BarCodeSerializer
    lookup_field = 'bar_code'


class UserBorrowInfo(viewsets.ViewSet):
    serializer_class = UserBorrowInfoSerializer
    queryset = BorrowInfo.objects.all()

    def list(self, request, user_username):
        # print(user_username)
        # uuser = User.objects.get(username=user_username)
        queryset = self.queryset.filter(user=user_username)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, user_username):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        bi = BorrowInfo(**serializer.validated_data)
        bi.user_id = user_username
        bi.save()
        serializer = self.serializer_class(bi)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BorrowInfoViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowInfoSerializer
    queryset = BorrowInfo.objects.all()
    lookup_field = 'id'
