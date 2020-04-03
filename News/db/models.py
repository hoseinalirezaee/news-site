from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    title = models.CharField(_('title'), max_length=512)
    summary = models.CharField(_('summary'), max_length=2000)
    main_image = models.URLField(_('main image'), max_length=1024)
    date_posted = models.DateTimeField(_('date posted'))
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    origin_id = models.PositiveIntegerField(_('origin id'))
    origin_url = models.URLField(_('origin url'), max_length=1024)

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


class Tag(models.Model):
    title = models.CharField(_('tag'), max_length=200)


class PostTag(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.PROTECT)
    tag = models.ForeignKey(to=Tag, on_delete=models.PROTECT)


class Category(models.Model):
    title = models.CharField(_('category'), max_length=200)
    parent = models.ForeignKey(
        to='self',
        on_delete=models.PROTECT,
        related_name='sub_categories',
        related_query_name='sub_categories'
    )


class Paragraph(models.Model):
    class Type(models.IntegerChoices):
        Text = 0
        Image = 1

    body = models.CharField(_('body'), max_length=5000)
    type = models.IntegerField(_('paragraph type'), choices=Type.choices)
    order = models.PositiveSmallIntegerField()

    post = models.ForeignKey(
        to='Post',
        on_delete=models.PROTECT,
        related_name='paragraphs',
        related_query_name='paragraphs'
    )
