from django.urls import path

from .views import PinklerUserAuthenticationView, PinklerUserRegistrationView, EmailConfirmationView
from .views import save_theme_preference, get_theme_preference

urlpatterns = [
    path('register/', PinklerUserRegistrationView.as_view(), name='register'),
    path('login/', PinklerUserAuthenticationView.as_view(), name='login'),
    path('confirm_email/<uuid:token>/', EmailConfirmationView.as_view(), name='confirm_email'),
    path('save-theme-preference/', save_theme_preference, name='save_theme_preference'),
    path('get-theme-preference/', get_theme_preference, name='get_theme_preference'),
]
