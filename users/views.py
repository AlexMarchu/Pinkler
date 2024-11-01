from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import PinklerUserCreationForm, PinklerUserAuthenticationForm


class PinklerUserRegistrationView(generic.CreateView):
    form_class = PinklerUserCreationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login')  # TODO: redirect to homepage with autologin

    def form_valid(self, form):
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PinklerUserAuthenticationView(LoginView):
    form_class = PinklerUserAuthenticationForm
    template_name = 'users/authentication.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        return super().form_valid(form)
