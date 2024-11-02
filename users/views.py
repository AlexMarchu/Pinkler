import uuid
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings

from .forms import PinklerUserCreationForm, PinklerUserAuthenticationForm
from .models import PinklerUser, EmailConfirmationToken


class PinklerUserRegistrationView(generic.CreateView):
    form_class = PinklerUserCreationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login')  # TODO: redirect to homepage with autologin

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        token_instance = EmailConfirmationToken.objects.create(user=user)

        confirmation_url = self.request.build_absolute_uri(
            reverse('confirm_email', kwargs={'token': token_instance.token})
        )

        subject = 'Подтвердите регистрацию в Pinkler'
        content = (f'Спасибо за регистрацию в нашей социальной сети!\n'
                   f'Для подтверждения своего email, перейдите по ссылке : \n{confirmation_url}')
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        try:
            send_mail(subject, content, from_email, recipient_list)
            print('Письмо успешно отправлено')
        except Exception as e:
            print(f'Ошибка при отправке письма {e}')

        return super().form_valid(form)


class EmailConfirmationView(View):
    def get(self, request, token):
        confirmation_token = get_object_or_404(EmailConfirmationToken, token=token)

        if not confirmation_token.is_valid():
            return render(request, 'users/token_invalid.html')

        user = confirmation_token.user
        user.is_active = True
        user.save()

        confirmation_token.delete()

        return render(request, 'users/confirm_email.html', {'user': user})


class PinklerUserAuthenticationView(LoginView):
    form_class = PinklerUserAuthenticationForm
    template_name = 'users/authentication.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        return super().form_valid(form)
