from django.conf.urls import url
from news_management import views

urlpatterns = [
    url(r'^article/$', views.ArticleList.as_view()),
    # url(r'^article/(?P<pk>[0-9]+)/$', ArticleDetail.as_view()),
    # url(r'^uc_article/', UncheckedArticleDestroy.as_view()),
    # url(r'^check/(?P<pk>[0-9]+)/$', check),
    url(r'^tag/$', views.TagList.as_view()),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagDetail.as_view()),
    url(r'^article/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view()),
    url(r'^get_ip/$', views.get_ip),
    url(r'^view/$', views.view),
    url(r'^setview/$', views.set_view),
]