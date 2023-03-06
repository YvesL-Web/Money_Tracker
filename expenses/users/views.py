from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from validate_email import validate_email

# Create your views here.
class RegisterView(View):
    def get(self, request):
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
       
       
    
