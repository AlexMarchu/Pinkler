import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class PinklerUser(AbstractUser):
    SEX_CHOICES = (
        ("Мужской", "М"),
        ("Женский", "Ж"),
    )

    is_active = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12, unique=True, blank=True, null=True)
    sex = models.CharField(max_length=7, choices=SEX_CHOICES, default="М")
    status = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='user/avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.__str__()


class EmailConfirmationToken(models.Model):
    user = models.OneToOneField(PinklerUser, on_delete=models.CASCADE)
    token = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() - self.created_at < timezone.timedelta(minutes=15)
