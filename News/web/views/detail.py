from django.views.generic.detail import DetailView

from db import models


class PostDetail(DetailView):
    model = models.Post
    context_object_name = 'post'
    template_name = 'post_detail.html'
