from rest_framework import authentication
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from . import permissions
from . import serializers


class PostViewSet(generics.CreateAPIView):
    serializer_class = serializers.PostSerializer
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.CanPost]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(data={'message': 'OK'}, status=status.HTTP_201_CREATED)


news_interface = PostViewSet.as_view()

__all__ = [
    'news_interface',
]
