from django.contrib import admin

from . import models

admin.site.register(models.Post)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.PostTag)
admin.site.register(models.User)
admin.site.register(models.TopPost)
admin.site.register(models.FavoriteAgency)
admin.site.register(models.UserFavoriteCategory)
admin.site.register(models.UserBookmark)
