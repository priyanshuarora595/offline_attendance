
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView 

from .forms import CustomPasswordResetForm
# from .views import UserProfileView

urlpatterns = [
    path('', views.index,name='index'),
    path('index', views.index,name='index'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('login',views.login,name='login'),
    path('logout',views.handlelogout,name='handlelogout'),
    path('signup',views.signup,name='signup'),
    path('handlelogin',views.handlelogin,name='handlelogin'),
    path('handlesignup',views.handlesignup,name='handlesignup'),
    path('mark_att', views.mark_att,name='mark_attendance'),
    path('download_file', views.download_file,name='download_file'),
    path('start_receiver', views.start_receiver,name='start_receiver'),
    path('stop_server', views.stop_server,name='stop_server'),
    path('thank_you', views.thank_you,name='thank_you'),
    path('userprofile/<str:id>', views.user_profile,name='user_profile'),
    path('del_user/<str:id>', views.del_user,name='del_user'),
    path('student', views.student,name='student'),
    path('teacher', views.teacher,name='teacher'),
    path('reset_list', views.reset_list,name='reset_list'),
    path('change_user_password', views.change_user_password,name='change_user_password'),
        
    path('reset_password/',
     auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm , template_name="accounts/password_reset.html"),
     name="reset_password"),
    
    # path('reset_password/',CustomPasswordResetView.as_view(template_name=))

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),
]
