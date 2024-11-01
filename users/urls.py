from django.urls import path

from .views import PinklerUserAuthenticationView, PinklerUserRegistrationView

urlpatterns = [
    path('register/', PinklerUserRegistrationView.as_view(), name='register'),
    path('login/', PinklerUserAuthenticationView.as_view(), name='login'),
]
