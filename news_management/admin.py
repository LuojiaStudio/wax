from django.contrib import admin
from .models import UncheckedArticle, Article, Tag

# Register your models here.
admin.site.register(UncheckedArticle)
admin.site.register(Article)
admin.site.register(Tag)