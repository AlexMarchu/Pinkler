import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model

from .models import Message

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.load_last_30_messages()
        content = {
            'command': 'fetch_messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        sender_instance = self.scope['user']
        message_content = data.get('message', '')
        image_data = data.get('image', '')

        message = Message(sender=sender_instance, content=message_content)
        if image_data:
            message.image = self.save_image(image_data)
        message.save()

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message),
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        return list(map(self.message_to_json, messages))

    def message_to_json(self, message):
        return {
            'sender': message.sender.username,
            'content': message.content,
            'timestamp': str(message.timestamp),
            'image': message.image.url if message.image else None
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    def save_image(self, image_data):
        import base64
        from django.core.files.base import ContentFile

        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        return ContentFile(base64.b64decode(imgstr), name=f'image.{ext}')

    def connect(self):
        try:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
            self.accept()
        except Exception as e:
            print(f"Error in connection: {e}")

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)
        self.commands[data_json['command']](self, data_json)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))


