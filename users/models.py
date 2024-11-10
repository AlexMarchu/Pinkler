import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings

class PinklerUser(AbstractUser):
    SEX_CHOICES = (
        ("Мужской", "М"),
        ("Женский", "Ж"),
    )

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=12, unique=True, blank=True, null=True)
    sex = models.CharField(max_length=7, choices=SEX_CHOICES, default="М")
    status = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars/', default='users/avatars/default_avatar.png', blank=True,
                               null=True)
    friends = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.__str__()

    def add_friend(self, user):
        if user != self:
            self.friends.add(user)
            user.friends.add(self)

    def remove_friend(self, user):
        self.friends.remove(user)
        user.friends.remove(self)

    def is_friends_with(self, user):
        return self.friends.filter(id=user.id).exists()

class EmailConfirmationToken(models.Model):
    user = models.OneToOneField(PinklerUser, on_delete=models.CASCADE)
    token = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() - self.created_at < timezone.timedelta(minutes=15)

    def __str__(self):
        return f'EmailConfirmationToken(user={self.user}, token={self.token})'

    def __repr__(self):
        return f'EmailConfirmationToken(user={self.user}, token={self.token}, created_at={self.created_at})'

class UserThemePreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="theme_preference")
    theme = models.CharField(max_length=50, default="light")
    font_size = models.CharField(max_length=10, default="16px")
    primary_color = models.CharField(max_length=7, default="#000000")

    def __str__(self):
        return f"Theme preferences for {self.user.username}"