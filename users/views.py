from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from .forms import PinklerUserCreationForm, PinklerUserAuthenticationForm
from .models import PinklerUser, EmailConfirmationToken
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserThemePreference
from django.http import JsonResponse



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

        return render(self.request, 'users/request_email_confirmation.html', {'user': user})


class EmailConfirmationView(View):
    def get(self, request, token):
        confirmation_token = get_object_or_404(EmailConfirmationToken, token=token)

        if not confirmation_token.is_valid():
            return render(request, 'users/token_invalid.html')

        user = confirmation_token.user
        user.is_active = True
        user.save()

        login(request, user)

        confirmation_token.delete()

        return render(request, 'users/email_confirmed.html', {'user': user})


class PinklerUserAuthenticationView(LoginView):
    form_class = PinklerUserAuthenticationForm
    template_name = 'users/authentication.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        return super().form_valid(form)

@csrf_exempt
def save_theme_preference(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        theme = data.get('theme')
        font_size = data.get('font_size')
        primary_color = data.get('primary_color')

        user_theme, created = UserThemePreference.objects.get_or_create(user=request.user)
        user_theme.theme = theme
        user_theme.font_size = font_size
        user_theme.primary_color = primary_color
        user_theme.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def get_theme_preference(request):
    user = request.user
    theme_preference = UserThemePreference.objects.get(user=user)
    return JsonResponse({
        'font_size': theme_preference.font_size,
        'primary_color': theme_preference.primary_color,
        'theme': theme_preference.theme,
    })
