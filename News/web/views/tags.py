from django.views.generic.list import ListView

from db import models


class TagsListView(ListView):
    model = models.Post
    ordering = '-date_posted'
    context_object_name = 'posts'
    paginate_by = 20
    template_name = 'tags.html'

    def get_queryset(self):
        tag = self.kwargs.get('tag')
        qs = models.Post.objects.filter(tags__title=tag)
        self.extra_context = {'tag': tag}
        return qs
