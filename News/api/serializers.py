from rest_framework import serializers

from db import models
from .categorymapper import map_category


class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=512)
    postUrl = serializers.URLField(max_length=1024)
    summary = serializers.CharField(allow_null=True, required=False, allow_blank=True, max_length=2000)
    mainImage = serializers.URLField(allow_null=True, required=False, max_length=1024)
    category = serializers.CharField(max_length=200)
    publishedDate = serializers.DateTimeField()
    postId = serializers.IntegerField(allow_null=True, required=False)
    paragraphs = serializers.JSONField()
    tags = serializers.ListField(child=serializers.CharField(), allow_null=True, required=False)
    agencyTitle = serializers.CharField(max_length=100, allow_null=False, required=True)
    agencyCode = serializers.CharField(max_length=100, allow_null=False, required=True)
    topPost = serializers.BooleanField(required=True)

    def create(self, validated_data):
        category = models.Category.objects.get(
            title=map_category(validated_data['category'])
        )

        agency = models.Agency.objects.get(
            code=validated_data['agencyCode']
        )

        post, created = models.Post.objects.get_or_create(
            title=validated_data['title'],
            defaults={
                'summary': validated_data['summary'],
                'main_image': validated_data['mainImage'],
                'date_posted': validated_data['publishedDate'],
                'origin_id': validated_data['postId'],
                'origin_url': validated_data['postUrl'],
                'category': category,
                'agency': agency
            }
        )

        if created:
            post.paragraphs = validated_data['paragraphs']
            models.Tag.objects.bulk_create(
                [models.Tag(title=tag) for tag in validated_data['tags']],
                ignore_conflicts=True
            )
            tags = models.Tag.objects.in_bulk(validated_data['tags'], field_name='title')
            models.PostTag.objects.bulk_create(
                [models.PostTag(tag=tag, post=post) for tag in tags.values()],
                ignore_conflicts=True
            )
            post.save()

        if validated_data['topPost'] is True:
            models.TopPost.objects.get_or_create(
                post=post,
                date_posted=post.date_posted
            )
            last_top_news = models.TopPost.objects.order_by('-date_posted')[:10]
            models.TopPost.objects.exclude(id__in=last_top_news).delete()

        return post
