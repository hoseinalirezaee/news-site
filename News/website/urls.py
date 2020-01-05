from django.urls import path
from website.views import Index, Detail, Category


urlpatterns = [
    path('', Index.as_view()),
    path('<id>/', Detail.as_view(), name='news_detail'),
    path('category/<str:category_name>/', Category.as_view())
]