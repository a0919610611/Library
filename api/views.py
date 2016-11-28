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

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.queryset)
        serializer.is_valid()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            Book.objects.create(**serializer.validated_data)
            return Response(
                serializer.validated_data,
                status=status.HTTP_201_CREATED
            )
        return Response({'error:some thing wrong'}, status=status.HTTP_400_BAD_REQUEST)
