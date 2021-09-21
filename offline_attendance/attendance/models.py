from django.db import models 
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views


# Create your models here.

SEMESTER_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
)

class StudentData(models.Model):
    username = models.CharField(max_length=50,primary_key=True)
    fullname = models.CharField(max_length=100)
    branch = models.CharField(max_length=30,null=True,blank=True)
    semester = models.CharField(
        max_length = 20,
        choices = SEMESTER_CHOICES,
        default = '1'
        )
    contact_number = models.CharField(max_length=10,null=True,blank=True)
    email_id = models.EmailField(max_length=100)
    
    def __str__(self):
        return self.fullname
    
    
class TeacherData(models.Model):
    username = models.CharField(max_length=50,primary_key=True)
    fullname = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10,null=True)
    email_id = models.EmailField(max_length=100)
    
    def __str__(self):
        return self.fullname
    
    
class StudentForm(ModelForm):
    class Meta:
        model = StudentData
        fields = '__all__'
        exclude = ['username']
        
        # def annss(id):
        #     user_data = StudentData.objects.filter(pk=id)
        
class TeacherForm(ModelForm):
    class Meta:
        model = TeacherData
        fields = '__all__'
        exclude = ['username']
        