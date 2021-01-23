from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import HashIndex
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    favorite_categories = models.ManyToManyField(
        to='Category',
        through='UserFavoriteCategory',
        related_name='users_who_favor'
    )

    bookmark = models.ManyToManyField(
        to='Post',
        through='UserBookmark',
        related_name='users_who_bookmark'
    )

    favorite_agencies = models.ManyToManyField(
        to='Agency',
        through='FavoriteAgency',
        related_name='users_who_favor'
    )


class Post(models.Model):
    title = models.CharField(_('title'), max_length=512, unique=True)

    summary = models.CharField(_('summary'), max_length=2000, null=True, blank=True)
    main_image = models.URLField(_('main image'), max_length=1024, null=True, blank=True)

    date_posted = models.DateTimeField(_('date posted'), default=now)
    date_created = models.DateTimeField(_('date created'), default=now)

    origin_id = models.CharField(_('origin id'), max_length=20, null=True, blank=True)
    origin_url = models.URLField(_('origin url'), max_length=1024)

    paragraphs = models.JSONField(db_index=True)

    agency = models.ForeignKey(
        'Agency',
        on_delete=models.PROTECT,
        related_name='posts',
        related_query_name='posts',
    )

    tags = models.ManyToManyField(
        to='Tag',
        through='PostTag',
        related_name='posts',
        related_query_name='posts'
    )

    category = models.ForeignKey(
        to='Category',
        on_delete=models.PROTECT,
        related_name='posts',
        related_query_name='posts'
    )

    class Meta:
        ordering = ('-date_posted', '-date_created')

        indexes = [
            models.Index(fields=('-date_posted', '-date_created'))
        ]

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.id})

    @property
    def breadcrumb(self):
        breadcrumb = []
        current = self.category

        while current:
            breadcrumb.insert(0, current)
            current = current.parent

        return breadcrumb

    @property
    def get_add_bookmark_url(self):
        return reverse('bookmark-add', kwargs={'post_id': self.id})


class TopPost(models.Model):
    post = models.OneToOneField(
        'Post',
        on_delete=models.CASCADE,
        related_name='top_posts',
        related_query_name='top_posts'
    )

    date_posted = models.DateTimeField(_('date posted'), default=now)

    class Meta:
        ordering = ('-date_posted',)

        indexes = [
            models.Index(fields=('-date_posted',))
        ]


class UserFavoriteCategory(models.Model):
    user = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        on_delete=models.PROTECT
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT
    )


class UserBookmark(models.Model):
    user = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        on_delete=models.PROTECT
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.PROTECT
    )

    @property
    def get_delete_url(self):
        return reverse('bookmark-delete', kwargs={'pk': self.id})


class Tag(models.Model):
    title = models.CharField(_('tag'), max_length=200, unique=True)

    class Meta:
        indexes = [
            HashIndex(fields=('title',))
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag-view', args=(self.title,))


class PostTag(models.Model):
    post = models.ForeignKey(to='Post', on_delete=models.PROTECT)
    tag = models.ForeignKey(to='Tag', on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'tag'], name='post_tag_unique')
        ]


class Category(models.Model):
    title = models.CharField(_('category'), max_length=200, unique=True)
    parent = models.ForeignKey(
        to='self',
        on_delete=models.PROTECT,
        related_name='sub_categories',
        related_query_name='sub_categories',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"{reverse('post-list-view')}?category={self.id}"


class Agency(models.Model):
    title = models.CharField(_('agency'), max_length=30, unique=True)
    code = models.CharField(_('code'), max_length=25, unique=True)
    image = models.URLField(_('image'), max_length=1024, null=True, blank=True)

    class Meta:
        indexes = [
            HashIndex(fields=['code']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"{reverse('post-list-view')}?agency={self.id}"


class FavoriteAgency(models.Model):
    user = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        on_delete=models.PROTECT
    )

    agency = models.ForeignKey(
        'Agency',
        on_delete=models.PROTECT
    )
