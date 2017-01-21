from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UncheckedArticleSerializer, ArticleSerializer
from .models import UncheckedArticle, Article
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication


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




