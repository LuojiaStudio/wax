from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .views import ArticleList
from .models import Article, UncheckedArticle


class ArticleApiTest(TestCase):
    def setUp(self):

        self.factory = APIRequestFactory()
        Article.objects.create(
            title='article',
            subtitle='article_subtitle',
            content='zzz',
            author=None,
            editor=None
        )
        UncheckedArticle.objects.create(
            title='unchecked_article',
            subtitle='article_subtitle',
            content='zzz',
            author=None,
            editor=None
        )

    def test_get_article_list_api(self):
        path = '/news/article/'
        request = self.factory.get(path, format='json')
        response = ArticleList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_unchecked_article_list_api(self):
        path = '/news/article/'
        data = {
            'unchecked': 1
        }
        request = self.factory.get(path, data, format='json')
        response = ArticleList.as_view()(request)
        self.assertEqual(response.status_code, 403)
        # TODO: forcing_auth

    def test_get_article_detail(self):
        path = '/news/article/1'
        request = self.factory.get(path)
        response = ArticleList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_unchecked_article_detail(self):
        pass

    def test_create_article(self):
        pass

    def test_delete_article(self):
        pass

    def test_check_article(self):
        pass



