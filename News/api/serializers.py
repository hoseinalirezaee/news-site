from django.db import IntegrityError
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

    def create(self, validated_data):
        category = models.Category.objects.get(
            title=map_category(validated_data['category'])
        )

        agency, created = models.Agency.objects.get_or_create(
            title=validated_data['agencyTitle'],
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

            for tag in validated_data['tags']:
                tag, created = models.Tag.objects.get_or_create(
                    title=tag
                )
                try:
                    models.PostTag.objects.create(
                        post=post,
                        tag=tag
                    )
                except IntegrityError:
                    pass

        post.save()
        return post
