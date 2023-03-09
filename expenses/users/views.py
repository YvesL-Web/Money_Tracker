from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout

from django.urls import reverse
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

import json
from validate_email import validate_email

from .utils import token_generator

# Create your views here.
class RegisterView(View):
    def get(self, request):
        return render(request,'users/register.html')
    
    def post(self, request):

        # get user data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # contain all previous post informations keep it visible
        context = {
            'fieldValues': request.POST
        }
        
        
        # validate data
        if not User.objects.filter(username=username).exists():
            if username == '':
                messages.error(request,'Provide an username')
                return render(request,'users/register.html',context)
            if not User.objects.filter(email=email).exists():
                if (password ==''):
                    messages.error(request,'password can not be empty')
                    return render(request,'users/register.html',context )              
                if len(password)<6 :
                    messages.error(request,'Password too short')
                    return render(request,'users/register.html',context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                # path_to_view
                # getting domains we're on
                # relative url to verification
                # encode uid
                # token
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('users:activate-email',kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})
                email_subject = "Activate your account."
                activate_url = 'http://'+domain+link
                email_body = f"Hi {username} ,Please use this link to activate your account\n {activate_url}"
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@test.com',
                    [email],
                    
                )
                email.send(fail_silently=False)
                messages.success(request,'Account successfully created')
                return render(request,'users/register.html' )
        
        return render(request,'users/register.html')
    

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({"username_error": "username should can not contain ! @ # & ( ) – [ { } ] : ; ', ? / *  ` ~ $ ^ + = < > “ "},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "username already used, choose another one."},status=409)
        return JsonResponse({"username_valid": True})
    
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({"email_error": "Invalid email."},status=400)
        if User.objects.filter(email=email):
            return JsonResponse({'email_error':"Email already used, choose another one."})
        return JsonResponse({"username_valid": True})
       
       
class VerificationView(View):
    def get(self,request, uidb64, token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not token_generator.check_token(user,token):            
                return redirect('login'+'?message='+'Account user already activated')
            
            if user.is_active:
                return redirect('users:login')
            user.is_active=True
            user.save()
            messages.success(request, 'Account successfully activated ')
            return redirect('users:login')
        except Exception as e:
            pass

        
        return redirect('users:login')
    

class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request,f"Welcome {user.get_username()}, you are now logged in.") 
                    return redirect('outlay:index')            
                messages.error(request,'Account is not active, please check your email.')
                return render(request,'users/login.html')      
            messages.error(request,'No Account with the given credentials. Verify your username/password')
            return render(request,'users/login.html')
        messages.info(request,'Please fill all fields.')
        return render(request,'users/login.html')
    
class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request,"You're now logged out.")
        return redirect('users:login')