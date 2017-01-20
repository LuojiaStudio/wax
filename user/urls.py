from django.conf.urls import url
from .views import login, change_password

urlpatterns = [
    url(r'^login/', login),
    url(r'change_pwd/', change_password)
]