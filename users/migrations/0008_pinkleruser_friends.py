# Generated by Django 5.1.2 on 2024-11-09 14:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_pinkleruser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='pinkleruser',
            name='friends',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
