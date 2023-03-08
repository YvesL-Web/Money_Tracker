from django.urls import path
from .views import RegisterView, UsernameValidationView, EmailValidationView, VerificationView
from django.views.decorators.csrf import csrf_exempt

app_name='users'

urlpatterns = [
    path('register',RegisterView.as_view(), name='register'),
    path('validate-username',csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('activate-email/<uidb64>/<token>',csrf_exempt(VerificationView.as_view()), name='activate-email'),
    
] 
