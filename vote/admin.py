from django.contrib import admin
from vote import models


admin.site.register(models.Activity)
admin.site.register(models.Group)
admin.site.register(models.Item)
admin.site.register(models.Vote)

