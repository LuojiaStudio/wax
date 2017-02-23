from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^login/', views.login),
    url(r'change_pwd/', views.change_password),
    url(r'^profile/$', views.Profile.as_view())
]