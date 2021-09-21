from django.contrib import admin
from .models import StudentData , TeacherData
# Register your models here.

admin.site.register(StudentData)
admin.site.register(TeacherData)