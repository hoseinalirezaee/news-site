from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('posts', views.PostViewSet, 'post')

urlpatterns = router.urls
