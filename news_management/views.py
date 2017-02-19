from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ArticleSerializer, TagSerializer
from .models import Article, Tag
from user.models import Staff
from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination
from rest_framework import generics
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from .permissions import IsNewsEditor
import django_filters.rest_framework
from django.views.decorators.csrf import csrf_exempt


class StandardResultsPagination(pagination.PageNumberPagination):
    page_size = 100
    page_query_param = 'page_size'
    max_page_size = 1000


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    )
    search_fields = ('title',)
    filter_fields = ('tags', )


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    )
    filter_fields = ('id', 'name', 'is_main', 'is_source')
    search_fields = ('name',),
    pagination_class = StandardResultsPagination


class TagDetail(APIView):

    def get_object(self, pk):
        try:
            return Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        print(Article.objects.get(pk=487).tags.all())
        tag = self.get_object(pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)



















