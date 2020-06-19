from django.views import generic

from db import models


class Index(generic.TemplateView):
    template_name = 'index.html'
    last_news_size = 8

    def get_context_data(self, **kwargs):
        last_news = self.get_last_news()

        context = super().get_context_data()
        context['last_news'] = last_news
        context['last_news_with_category'] = self.get_last_news_with_category()
        return context

    def get_last_news(self):
        last_news_queryset = models.Post.objects.filter(main_image__isnull=False) \
                                 .order_by('-date_posted')[:self.last_news_size]
        return last_news_queryset

    def get_last_news_with_category(self):
        root_categories = models.Category.objects.filter(parent__isnull=True).exclude(
            title='سایر'
        )
        last_news = {}
        for category in root_categories:
            posts = models.Post.objects \
                        .filter(category__in=category.sub_categories.all(), main_image__isnull=False) \
                        .order_by('-date_posted')[:3]
            last_news[category] = posts

        return last_news
