# Generated by Django 5.1.2 on 2024-11-05 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_remove_message_receiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='chat_images/'),
        ),
    ]