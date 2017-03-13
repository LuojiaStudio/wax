from django.conf.urls import url
from vote import views

urlpatterns = [
    url(r'^activity/$', views.ActivitySet.as_view({'get': 'list'})),
    url(r'^activity/(?P<pk>[0-9]+)/$', views.ActivitySet.as_view({'get': 'retrieve'})),

    url(r'^group/$', views.GroupSet.as_view({'get': 'list'})),
    url(r'^group/(?P<pk>[0-9]+)/$', views.GroupSet.as_view({'get': 'retrieve'})),

    url(r'^item/$', views.ItemSet.as_view({'get': 'list'})),
    url(r'^item/(?P<pk>[0-9]+)/$', views.ItemSet.as_view({'get': 'retrieve'})),

    url(r'vote/$', views.ListAndCreateVote.as_view())
]