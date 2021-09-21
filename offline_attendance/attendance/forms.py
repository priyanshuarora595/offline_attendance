from django.contrib.auth import views as auth_views
from django.contrib import messages
from django import forms
from .models import StudentData
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=100)
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        all_emails=list(StudentData.objects.all().values_list('email_id', flat=True))
        if email not in all_emails:
            # raise messages.warning(request, 'Do no Spam Other Emails!!')
            raise forms.ValidationError('Do not Spam Other Emails!!',code='invalid')
        
        return email


