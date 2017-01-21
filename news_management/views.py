from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UncheckedArticleSerializer, ArticleSerializer
from .models import UncheckedArticle, Article
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from .permissions import IsNewsEditor


class ArticleList(APIView):
    """
    List all articles or create new one
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get(self, request):
        if 'unchecked' in request.GET:
            if request.user.has_perm('news_management.add_uncheckedarticle'):
                unchecked_articles = UncheckedArticle.objects.all()
                serializer = UncheckedArticleSerializer(unchecked_articles, many=True)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            article = Article.objects.all()
            serializer = ArticleSerializer(article, many=True)
            return Response(serializer.data)

    def post(self, request):
        if request.user.has_perm('news_management.add_article'):
            serializer = ArticleSerializer(data=request.data)
            self.create(serializer)
        elif request.user.has_perm('news_management.add_uncheckedarticle'):
            serializer = UncheckedArticleSerializer(data=request.data)
            self.create(serializer)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def create(serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetail(APIView):
    """
    Retrieve, update or delete a article or an unchecked article
    """
    @staticmethod
    def get_article_object(pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    @staticmethod
    def get_unchecked_article_object(pk):
        try:
            return UncheckedArticle.objects.get(pk=pk)
        except UncheckedArticle.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        if 'unchecked' in request.GET:
            if request.user.has_perm('news_management.add_uncheckedarticle'):
                article = self.get_unchecked_article_object(pk)
                serializer = UncheckedArticleSerializer(article)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            article = self.get_article_object(pk)
            serializer = ArticleSerializer(article)
        return Response(serializer.data)

    @permission_required('news_management.change_article')
    def put(self, request, pk):
        article = self.get_article_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_required('news_management.delete_article')
    def delete(self, request, pk):
        article = self.get_article_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UncheckedArticleDestroy(generics.DestroyAPIView):
    """
    Destroy unchecked article
    """
    queryset = UncheckedArticle.objects.all()
    serializer_class = UncheckedArticleSerializer
    permission_classes = (IsNewsEditor, )
















