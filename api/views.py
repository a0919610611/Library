from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, generics, viewsets, status
from api.serializers import *
from datetime import datetime
from api.models import *


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
