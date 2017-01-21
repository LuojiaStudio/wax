from rest_framework import serializers
from .models import UncheckedArticle, Article
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


class UncheckedArticleSerializer(BaseArticleSerializer):

    class Meta:
        model = UncheckedArticle


class ArticleSerializer(BaseArticleSerializer):

    class Meta:
        model = Article
