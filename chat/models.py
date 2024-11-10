from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # @staticmethod
    # def load_last_30_messages():
    #     return Message.objects.order_by('-timestamp').all()[:50][::-1]

    def __str__(self):
        return f'Message from {self.sender}: {self.content}'

    def __repr__(self):
        return self.__str__()


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)

    def load_last_50_messages(self):
        return self.messages.objects.order_by('-timestamp').all()[:50][::-1]

    def __str__(self):
        return f'Chat {self.pk}'
