from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import PinklerUser


class PinklerUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'placeholder': 'Имя пользователя',
            'required': 'required',
            'autofocus': 'autofocus'
        })
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'required': 'required'
        })
    )

    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Подтвердите пароль',
            'required': 'required'
        })
    )

    # TODO: Add an interface for changing data in the user profile page.
    """
    These fields are not needed during registration,
    but will be needed in the future.
    For now, I'll just leave it here.
    """

    # phone_number = forms.CharField(
    #     label='Номер телефона',
    #     widget=forms.TextInput(attrs={
    #         'placeholder': 'Номер телефона',
    #     })
    # )
    #
    # sex = forms.ChoiceField(
    #     label='Пол',
    #     choices=SEX_CHOICES,
    #     initial='М',
    #     widget=forms.Select(attrs={
    #         'required': 'required'
    #     })
    # )
    #
    # status = forms.CharField(
    #     label='Статус',
    #     widget=forms.Textarea(attrs={
    #         'placeholder': 'Введите свой статус',
    #         'rows': 3,
    #         'cols': 40,
    #         'required': 'false'
    #     }),
    #     required=False
    # )
    #
    # birthday = forms.DateField(
    #     label='Дата рождения',
    #     widget=forms.DateInput(attrs={
    #         'type': 'date',
    #         'required': 'false'
    #     }),
    #     required=False
    # )
    #
    # avatar = forms.ImageField(
    #     label='Аватар',
    #     required=False
    # )

    class Meta:
        model = PinklerUser
        fields = ('username', 'password1', 'password2')


class PinklerUserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'placeholder': 'Имя пользователя',
            'required': 'required',
            'autofocus': 'autofocus',
        })
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'required': 'required',
        })
    )

    class Meta:
        model = PinklerUser
        fields = ('username', 'password')
