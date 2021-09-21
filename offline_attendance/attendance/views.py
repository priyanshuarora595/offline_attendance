from django.shortcuts import render , redirect
from offline_attendance.settings import MEDIA_ROOT
from datetime import date
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate ,login as auth_login , logout , update_session_auth_hash
from attendance.models import StudentData , TeacherData , StudentForm , TeacherForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm , SetPasswordForm
import random



media_path = str(MEDIA_ROOT)


# Create your views here.
valid_username='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890'
attendees={}
attendees_user_ip={}
index_content={'status':len(attendees),'download_link':""}

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    
    if request.session.get('user')=='student' and StudentData.objects.filter(username=request.user).exists():
        return redirect(student)
    elif request.session.get('user')=='teacher' and TeacherData.objects.filter(username=request.user).exists():
        request.session['start_btn']=1
        if request.session['pin'] :
            request.session['stop_btn']=1    
        else:
            request.session['stop_btn']=0
        return redirect(teacher)
    
    else:
        request.session['start_btn']=1
        return render(request, 'index.html',index_content)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def mark_att(request):
    if request.method == "POST":
            name = list(StudentData.objects.filter(username=request.user).values_list('fullname',flat=True))[0]
            class_pin_rcvd=request.POST.get("class_pin_name")
            user_ip=get_client_ip(request)
            print(user_ip)
            if class_pin_rcvd not in attendees.keys():
                messages.error(request, 'Incorrect Pin ! Please Re-try!')
                return redirect(index)
            else:
                if user_ip in attendees_user_ip[str(class_pin_rcvd)]:
                    # attendees_user_ip[str(class_pin_rcvd)].append(user_ip)
                    # print(attendees_user_ip)
                    return render(request, 'error.html')
                else:
                    attendees[str(class_pin_rcvd)].append(name)
                    attendees_user_ip[str(class_pin_rcvd)].append(user_ip)
                    request.session['count'] = 1
                    return redirect(thank_you)


def start_receiver(request):
    request.session['error'] = ""
    if TeacherData.objects.filter(username=request.user).exists():
        global media_path
        request.session['stop_btn']=1
        request.session['start_btn']=0
        request.session['download_btn']=0
        class_pin = random.randint(100000, 999999)
        while class_pin in attendees.keys():
            class_pin = random.randint(100000, 999999)
        request.session['pin'] = class_pin
        attendees[str(class_pin)]=[]
        attendees_user_ip[str(class_pin)]=[]
        date_var=str(date.today())
        media_path_session=  media_path+f"\\attendance_{request.user}_{class_pin}_{date_var}.csv"
        request.session['download_link'] = media_path_session
        attendees_sorted=[]
        index_content['status']=len(attendees)
        return redirect('teacher')
    else:
        return render(request, 'error.html')


def stop_server(request):
    if TeacherData.objects.filter(username=request.user).exists():
        request.session['start_btn']=1
        request.session['download_btn']=1
        request.session['stop_btn']=0
        index_content['status']=len(attendees)
        if str(request.session['pin']) in attendees.keys():
            if len(attendees[str(request.session['pin'])])>0: 
                with open(request.session['download_link'],'a') as out_file:
                    out_file.write(str(date.today()))
                    out_file.write("\n")
                    attendees_sorted = sorted(list(set(attendees[str(request.session['pin'])])))
                    for std_name in attendees_sorted:
                        out_file.write(std_name)
                        out_file.write("\n")
                # print(attendees)
                del attendees[str(request.session['pin'])]
                del attendees_user_ip[str(request.session['pin'])]
                # print(attendees)
                index_content['status']=len(attendees)
                request.session['pin']=''
                return redirect('teacher')
            else:
                del attendees[str(request.session['pin'])]
                request.session['error'] = "no student entry!"
                request.session['pin']=''
                return redirect('teacher')
        else:
            return render(request, 'index.html',index_content)
    else:
        return render(request, 'error.html')

def download_file(request):
    # print("here")
    full_url_try=str(request.session['download_link'])
    full_url= str(request.session['download_link']).split("\media")
    file_name=full_url[1][1:]
    # full_url='\media'+full_url[1]
    # print(full_url)
    # full_url=full_url.replace('\\','/')
    request.session['stop_btn']=1
    request.session['start_btn']=0
    request.session['download_btn']=0
    # return redirect(str(full_url))
    with open(str(full_url_try), 'r') as f:
           file_data = f.read()
    return HttpResponse(file_data,
                        headers={
                            'Content-Type': 'text/csv',
                            'Content-Disposition': f'attachment;filename={file_name}'})

def login(request):
    if request.user.is_authenticated:
        return redirect(index)
    else:
        return render(request, 'login.html')

def student(request):
    if StudentData.objects.filter(username=request.user).exists():
        request.session['start_btn']=1
        return render(request, 'student.html',index_content)
    else:
        return render(request, 'error.html')

def teacher(request):
    if TeacherData.objects.filter(username=request.user).exists():
        request.session['start_btn']=1
        return render(request, 'teacher.html',index_content)
    else:
        return render(request, 'error.html')

def handlelogin(request):
    
    if request.method == "POST":
        #Get parameters
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        
        user = authenticate(username=username,password=password)
        
        if user is not None:
            auth_login(request,user)
            messages.success(request, 'Successfully logged in')
            if StudentData.objects.filter(username=user).exists():
                # index_context['choice'] = 'student'
                request.session['user'] = 'student'
                request.session['count'] = 0
                index_content['status']=len(attendees)
                return redirect(student)
                # request.session['status'] = 0
            elif TeacherData.objects.filter(username=user).exists():
                # index_context['choice'] = 'teacher'
                request.session['user'] = 'teacher'
                request.session['count'] = 0
                request.session['download_link'] = None
                index_content['status']=len(attendees)
                # request.session['status'] = 0
                return redirect(teacher)
            elif username == "admin":
                return redirect(index)
                

        
        else:
            messages.error(request, 'Invalid Credentials ! Please try again .')
            return redirect('login')
    
    else:
        return HttpResponse('404 - Not Found')

def handlelogout(request):
    logout(request)
    messages.success(request, 'Successfully logged Out.')
    return redirect('index')


def signup(request):
    if request.user.is_authenticated:
        return redirect(index)
    else:
        return render(request, 'signup.html')
        

def handlesignup(request):
    
    if request.method == "POST":
        #Get parameters
        username = request.POST['username']
        fullname = (request.POST['fullname']).title()
        EmailAddress = request.POST['EmailAddress']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # choice = request.POST['choice']
        
        #check for errorneous input
        if len(username)>20:
            messages.error(request, "username length not more than 20 allowed")
            return render(request, 'signup.html')
        
        if  len(pass1)<8:
            messages.error(request, "minimum length of password = 8")
            return render(request, 'signup.html')
        
        if pass1 != pass2:
            messages.error(request, "passwords do not match")
            return render(request, 'signup.html')
            
        for c in username:
            if c not in valid_username:
                messages.error(request, "username can contain letter , numbers and underscore ( _ ) only!")
                return render(request, 'signup.html')
        emails=list(StudentData.objects.all().values_list('email_id', flat=True)) 
        
        if EmailAddress in emails:
            messages.error(request, "Email Address Exists !!")
            return render(request, 'signup.html')
        user = authenticate(username=username,password=pass1)
        
        if user is None:
            #create user
            myuser=User.objects.create_user(username,email=EmailAddress,password=pass1)
            myuser.fullname = fullname
            myuser.save()
            
            new_user = StudentData(username=username,fullname=fullname,email_id=EmailAddress)

            new_user.save()
            messages.success(request, "Your Account has been successfully created")
            return redirect('login')

        else:
            messages.error(request, "Username already exists!!")
            return render(request, 'signup.html')
    
    else:
        return HttpResponse('404 - Not Found')
    
    
def thank_you(request):
    # user_ip=get_client_ip(request)
    # print(user_ip)
    # class_pin=request.session['pin']
    # attendees_user_ip[str(class_pin)].append(user_ip)
    # print(attendees_user_ip)
    return render(request, 'thank_you.html')

def user_profile(request,id):
    if str(request.user) != str(id):
        messages.warning(request, 'You cant view someone else profile!')
        return redirect(index)
    
    if request.method=="POST":
        if StudentData.objects.filter(username=request.user).exists():
            user_data=StudentData.objects.get(pk=id)
            f = StudentForm(request.POST,instance=user_data)
            new_email_id = request.POST['email_id']
            # User.objects.filter(username=request.user).update(email=new_email_id)
            messages.success(request, 'Profile updated successfully!!')
            f.save()
        elif TeacherData.objects.filter(username=request.user).exists():
            user_data=TeacherData.objects.get(pk=id)
            f = TeacherForm(request.POST,instance=user_data)
            new_email_id = request.POST['email_id']
            messages.success(request, 'Profile updated successfully!!')
            f.save()
        User.objects.filter(username=request.user).update(email=new_email_id)
    else:
        if StudentData.objects.filter(username=request.user).exists():
            user_data=StudentData.objects.get(pk=id)
            f = StudentForm(instance=user_data)
        elif TeacherData.objects.filter(username=request.user).exists():
            user_data=TeacherData.objects.get(pk=id)
            f = TeacherForm(instance=user_data)
    
    form_context = {'form':f}
    return render(request, 'userprofile.html',form_context)
    
    
def del_user(request,id):
    
    if str(request.user) != str(id):
        messages.warning(request, 'You cant delete someone else profile!')
        return redirect(index)
    
    if StudentData.objects.filter(username=request.user).exists():
        user_data=StudentData.objects.get(pk=id)
        u=User.objects.get(username = request.user)
        
    elif TeacherData.objects.filter(username=request.user).exists():
        user_data=TeacherData.objects.get(pk=id)
        u=User.objects.get(username = request.user)
       
    logout(request) 
    user_data.delete()
    u.delete()
    
    messages.success(request, 'Account deleted Successfully!!')
    
    return redirect(signup)


def change_user_password(request):
    if request.user.is_authenticated:  
        if request.method =="POST":
            fm = PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
            else:
                fm.save()
            update_session_auth_hash(request,fm.user)
            red='userprofile/'+str(request.user)
            messages.success(request, 'Password Changed Successfully!!')
            return HttpResponseRedirect(red)
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'change_user_password.html',{'form':fm})
    else:
        return redirect('login')
    
    
def reset_list(request):
    index_content['status'] = 0
    global attendees
    global attendees_user_ip
    print(attendees)
    print(attendees_user_ip)
    attendees={}
    attendees_user_ip={}
    messages.success(request,'All Entries has been cleared!')
    return redirect(index)