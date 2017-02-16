from rest_framework import serializers
from .models import Article, Tag
from user.models import Staff


class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        fields = (
            'title',
            'author',
            'create_staff',
            'checked_staff',
            'cover',
            'create_time',
            'humaniza_create_time',
            'last_modify_time',
            'issuing_time',
            'is_checked',
            'tags',
            'view_number',
            'like_number',
            'content',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'is_main', 'is_source')
