# Generated by Django 5.1.2 on 2024-11-10 17:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='bookmark',
            field=models.ManyToManyField(blank=True, related_name='bookmarks', to=settings.AUTH_USER_MODEL),
        ),
    ]
