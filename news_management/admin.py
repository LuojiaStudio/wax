from django.contrib import admin
from .models import Article, Tag, View, Like

# Register your models here.
admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(View)
admin.site.register(Like)