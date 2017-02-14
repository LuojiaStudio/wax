from django.conf.urls import url
from .views import ArticleList, TagList

urlpatterns = [
    url(r'^article/$', ArticleList.as_view()),
    # url(r'^article/(?P<pk>[0-9]+)/$', ArticleDetail.as_view()),
    # url(r'^uc_article/', UncheckedArticleDestroy.as_view()),
    # url(r'^check/(?P<pk>[0-9]+)/$', check),
    url(r'tag/$', TagList.as_view()),
]