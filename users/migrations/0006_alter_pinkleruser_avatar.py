# Generated by Django 5.1.2 on 2024-11-07 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_pinkleruser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pinkleruser',
            name='avatar',
            field=models.ImageField(blank=True, default='users/avatars/default.png', null=True, upload_to='users/avatars/'),
        ),
    ]
