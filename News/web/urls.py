from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.Index.as_view()),
    re_path(r'^posts/(?P<pk>\d+)/$', views.PostDetail.as_view(), name='post-detail'),
    path('posts/', views.PostsListView.as_view(), name='post-list-view'),
    path('signup/success/', views.SignUpSuccessView.as_view(), name='signup_success'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/success/', views.LoginSuccessView.as_view(), name='login-success'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
