from django.urls import path
from .views import RegisterView, UsernameValidationView, EmailValidationView, VerificationView, LoginView,LogoutView,ResetPassword,CompletePasswordReset
from django.views.decorators.csrf import csrf_exempt

app_name='users'

urlpatterns = [
    path('register',RegisterView.as_view(), name='register'),
    path('login',LoginView.as_view(), name='login'),
    path('logout',LogoutView.as_view(), name='logout'),
    path('reset-password',ResetPassword.as_view(), name='reset-password'),

    path('validate-username',csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('activate-email/<uidb64>/<token>',VerificationView.as_view(), name='activate-email'),
    path('set-new-password/<uidb64>/<token>',CompletePasswordReset.as_view(), name='set-new-password'),
    
] 
