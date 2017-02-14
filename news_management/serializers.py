from rest_framework import serializers
from .models import Article, Tag
from user.models import Staff


class BaseArticleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'title',
            'subtitle',
            'author',
            'editor',
            'create_time',
            'last_modify_time',
            'tags',
            'view_number',
            'like_number',
            'content',
        )


class ArticleSerializer(BaseArticleSerializer):

    class Meta:
        model = Article


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'is_main', 'is_source')
