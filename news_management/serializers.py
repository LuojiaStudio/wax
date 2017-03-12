from rest_framework import serializers
from .models import Article, Tag
from user.models import Staff


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'is_main', 'is_source')


class ArticleSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(many=True)

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'author',
            'photographer',
            'create_staff',
            'checked_staff',
            'cover',
            'create_time',
            'humaniza_create_time',
            'last_modify_time',
            'issuing_time',
            'is_checked',
            'is_homepage',
            'is_notice',
            'tags',
            'tags_str',
            'view_number',
            'like_number',
            'content',
        )

