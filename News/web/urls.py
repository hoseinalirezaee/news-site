from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.Index.as_view()),
    re_path(r'^posts/(?P<pk>\d+)/$', views.PostDetail.as_view(), name='post-detail'),
    path('posts/', views.PostsListView.as_view(), name='post-list-view')
]
