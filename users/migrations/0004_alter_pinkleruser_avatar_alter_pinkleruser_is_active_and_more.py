import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_pinkleruser_is_active_emailconfirmationtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pinkleruser',
            name='avatar',
            field=models.ImageField(blank=True, default='images/avatars/man.png', null=True, upload_to='users/avatars/'),
        ),
        migrations.AlterField(
            model_name='pinkleruser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='UserThemePreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(default='light', max_length=50)),
                ('font_size', models.CharField(default='16px', max_length=10)),
                ('primary_color', models.CharField(default='#000000', max_length=7)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='theme_preference', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
