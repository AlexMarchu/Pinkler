from django.db import models
from django.conf import settings


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def load_last_30_messages():
        return Message.objects.order_by('timestamp').all()[:50]

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}: {self.content}'

    def __repr__(self):
        return self.__str__()
