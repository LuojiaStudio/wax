from django.conf.urls import url
from .views import ArticleList

urlpatterns = [
    url(r'^article/', ArticleList.as_view())
]