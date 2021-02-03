from django.urls import path

from .views import news_interface

urlpatterns = [
    path('posts/', news_interface),
]
