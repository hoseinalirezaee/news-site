from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.http.response import HttpResponse
from common.models import News


class Index(View):

    def get(self, request):

        str = ''
        # get root categories from database
        root_categories_query_set = News.objects.values('root_category').distinct()
        root_categories = [root_cat['root_category'] for root_cat in root_categories_query_set]

        # get latest news from database
        latest_news_query_set = News.objects.all().order_by('-publish_date', '-publish_time')[:8]
        latest_news = [lat_news for lat_news in latest_news_query_set]

        # get latest news from each root category
        latest_news_on_each_category = {}
        for root_category in root_categories:
            latest_news_on_cat = News.objects\
                .filter(root_category=root_category)\
                .order_by('-view_count', '-publish_date', '-publish_time')[:4]
            latest_news_on_each_category[root_category] = [news for news in latest_news_on_cat]

        # get important posts slide bar
        important_posts_slide_bar_query_set = News.objects.all().order_by('-publish_date', '-publish_time')[:5]
        important_posts_slide_bar = [item for item in important_posts_slide_bar_query_set]

        # get important post
        important_posts_query_set = News.objects.all().order_by('-publish_date', '-publish_time')[:2]
        important_posts = [item for item in important_posts_query_set]

        context = {
            'root_categories': root_categories,
            'latest_news': latest_news,
            'latest_news_on_each_category': latest_news_on_each_category,
            'important_posts_slide_bar': important_posts_slide_bar,
            'important_post': important_posts
        }

        return render(
            request,
            'index.html',
            context=context
        )


class Detail(View):

    def get(self, request, id):
        post = News.objects.get(id=id)
        post.view_count += 1
        post.save()

        context = {
            'post': post
        }

        return render(
            request,
            'detail.html',
            context=context
        )


class Category(ListView):

    model = News
    paginate_by = 20
    template_name = 'category_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        queryset = News.objects.filter(root_category=category_name)
        self.extra_context = {'category_name': category_name}
        return queryset

    # def get(self, reqeust, category_name):
    #
    #     posts_query_set = News.objects.filter(root_category=category_name)[:30]
    #
    #     context = {
    #         'category_name': category_name,
    #         'posts': posts_query_set
    #     }
    #
    #     return render(
    #         reqeust,
    #         'category_list.html',
    #         context=context
    #     )
