from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ArticleSerializer, TagSerializer
from .models import Article, Tag, View
from user.models import Staff, Student
from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination, request
from rest_framework import generics
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib.auth.decorators import permission_required
from .permissions import IsNewsEditor
import django_filters.rest_framework
from django.views.decorators.csrf import csrf_exempt
import json


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
    filter_fields = ('tags', 'is_checked')
    authentication_classes(IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data=request.data
        student = Student.objects.get(user=request.user)
        staff = Staff.objects.get(student=student)
        data['create_staff'] = staff.id
        if (request.user.has_perm('news_management.can_check_article')):
            data['checked_staff'] = staff.id
            data['is_checked'] = True
        else:
            data['is_checked'] = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        tag = self.get_object(pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)


class ArticleDetail(APIView):

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self,request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def get_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return JsonResponse({'ip': ip})


@csrf_exempt
def view(request):
    print(request.body)
    data = json.loads(request.body.decode())
    print(data)
    article_id = data['id']
    ip = data['ip']
    article_view = View(ip=ip, article=Article.objects.get(pk=article_id))
    article_view.save()

    response = HttpResponse()
    response.status_code = 200

    return response



















