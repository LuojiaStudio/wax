from django.conf.urls import url
from .views import upload_to_OSS

urlpatterns = [
    url(r'up/$', upload_to_OSS)
]