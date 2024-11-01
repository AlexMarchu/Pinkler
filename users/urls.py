from django.urls import path

from .views import PinklerUserAuthenticationView, PinklerUserRegistrationView, EmailConfirmationView

urlpatterns = [
    path('register/', PinklerUserRegistrationView.as_view(), name='register'),
    path('login/', PinklerUserAuthenticationView.as_view(), name='login'),
    path('confirm_email/<uuid:token>/', EmailConfirmationView.as_view(), name='confirm_email'),
]
