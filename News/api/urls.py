from django.urls import path

from News.api.views import news_interface

urlpatterns = [
    path('posts/', news_interface),
]
