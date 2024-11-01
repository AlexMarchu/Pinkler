from django.db import models
from django.contrib.auth.models import AbstractUser


class PinklerUser(AbstractUser):
    SEX = (
        ("Мужской", "М"),
        ("Женский", "Ж"),
    )

    phone_number = models.CharField(max_length=12, unique=True)
    sex = models.CharField(max_length=7, choices=SEX, default="Мужчина")
    status = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='user/avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.__str__()
