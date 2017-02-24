from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission
# Register your models here.

admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(School)
admin.site.register(Dormitory)
admin.site.register(Area)
admin.site.register(Faculty)
admin.site.register(JobTitle)
admin.site.register(StudentUnion)
admin.site.register(Department)
admin.site.register(Permission)
