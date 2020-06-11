from django.http.response import Http404
from django.urls import reverse
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import response
from rest_framework import serializers
from rest_framework import validators
from rest_framework.views import APIView

from db import models


class BookmarksListView(ListView):
    paginate_by = 5
    template_name = 'bookmarks.html'
    context_object_name = 'bookmarks'

    def get_queryset(self):
        user = self.get_user()
        return models.UserBookmark.objects.filter(user=user)

    def get_user(self):
        user = self.request.user
        if user.is_authenticated:
            return user
        raise Http404()


class BookmarkDeleteView(DeleteView):
    model = models.UserBookmark

    def get_success_url(self):
        return reverse('bookmarks')

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return models.UserBookmark.objects.filter(user=user)
        raise Http404()


class AddBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserBookmark
        fields = ['user', 'post']
        validators = [
            validators.UniqueTogetherValidator(
                models.UserBookmark.objects.all(),
                ['user', 'post']
            )
        ]


class AddToBookmarkView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, post_id):
        post = models.Post.objects.get(id=post_id)
        user = self.request.user

        serializer = AddBookmarkSerializer(data={'user': user.id, 'post': post.id})
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'ok'}, status=200)
        else:
            return response.Response({'message': 'error'}, status=409)
