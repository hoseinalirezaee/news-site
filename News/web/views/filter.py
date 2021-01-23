from django.views.generic.list import ListView

from db import models
from ..filters import PostFilterSet


class PostsListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    paginate_by = 20
    template_name = 'posts_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_set = PostFilterSet(self.request.GET, queryset)
        self.extra_context = {'filter_set': filter_set}
        return filter_set.qs.cache()
