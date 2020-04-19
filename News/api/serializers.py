from django.db import IntegrityError
from rest_framework import serializers

from db import models
from .categorymapper import map_category


class PostSerializer(serializers.Serializer):
    title = serializers.CharField()
    postUrl = serializers.URLField()
    summary = serializers.CharField(allow_null=True, allow_blank=True)
    mainImage = serializers.CharField(allow_null=True, allow_blank=True)
    category = serializers.CharField()
    dateTime = serializers.DateTimeField()
    postId = serializers.RegexField(r'\d+', max_length=20, allow_blank=True, allow_null=True)
    paragraphs = serializers.JSONField()
    tags = serializers.ListField(child=serializers.CharField(), allow_null=True, allow_empty=True)
    agencyTitle = serializers.CharField()
    agencyCode = serializers.CharField()

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
                'date_posted': validated_data['dateTime'],
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
