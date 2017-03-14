from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^login/', views.login),
    url(r'change_pwd/', views.change_password),
    url(r'^profile/$', views.Profile.as_view()),
    url(r'^has_perm/', views.has_perm),
    url(r'^check_whu_student/$', views.check_whu_student),
    url(r'^login_or_register/$', views.login_or_register)
]