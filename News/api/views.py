from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from . import serializers


class PostViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    serializer_class = serializers.PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data={'message': 'OK'}, status=status.HTTP_201_CREATED)
