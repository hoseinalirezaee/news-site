from django.urls import path
from website.views import Index, Detail, Category, Search


urlpatterns = [
    path('', Index.as_view()),
    path('post/<id>/', Detail.as_view(), name='news_detail'),
    path('category/<str:category_name>/', Category.as_view()),
    path('search/', Search.as_view())
]