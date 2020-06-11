from django.http.request import HttpRequest
from django.views.generic.detail import DetailView

from db import models


class PostDetail(DetailView):
    model = models.Post
    context_object_name = 'post'
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        request: HttpRequest = self.request
        context['bookmark_add_url'] = request.build_absolute_uri(post.get_add_bookmark_url)
        return context
