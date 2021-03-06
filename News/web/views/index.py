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
        top_news = self.get_top_news()
        top_news_count = top_news.count()
        try:
            context['top_new_left'] = top_news[top_news_count - 2:top_news_count]
        except AssertionError:
            pass
        if 'top_new_left' in context:
            context['top_news_slider'] = top_news.exclude(id__in=context['top_new_left'])
        if self.request.user.is_authenticated:
            agencies = self.request.user.favorite_agencies.all()
            cats = self.request.user.favorite_categories.all()
            categories = set()
            for cat in cats:
                if cat.parent is None:
                    sub_cats = models.Category.objects.filter(parent=cat)
                    categories = categories.union(set(sub_cats))
                else:
                    categories.add(cat)
            recommended = models.Post.objects \
                              .filter(agency__in=agencies, category__in=categories) \
                              .order_by('-date_posted')[:8]
            context['recommended'] = recommended
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

    def get_top_news(self):
        posts = models.TopPost.objects.all().order_by('-date_posted')
        return posts
