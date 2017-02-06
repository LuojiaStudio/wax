from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .views import ArticleList


class ArticleApiTest(TestCase):
    def setUp(self):

        self.factory = APIRequestFactory()

    def test_list_article_api(self):
        path = '/news/article/'
        data = {
            'unchecked': 1
        }

        request = self.factory.get(path, data, format='json')
        response = ArticleList.as_view()(request)


