from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('posts/', views.PostsListView.as_view(), name='post-list-view'),
    path('signup/success/', views.SignUpSuccessView.as_view(), name='signup_success'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/success/', views.LoginSuccessView.as_view(), name='login-success'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('bookmarks/', views.BookmarksListView.as_view(), name='bookmarks'),
    path('bookmarks/<int:pk>/', views.BookmarkDeleteView.as_view(), name='bookmark-delete'),
    path('bookmarksAdd/<int:post_id>/', views.AddToBookmarkView.as_view(), name='bookmark-add'),
    path('tags/<str:tag>/', views.TagsListView.as_view(), name='tag-view')
]
