# Generated by Django 4.1.2 on 2022-11-09 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_is_superuser_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.TextField(choices=[('user', 'USER'), ('admin', 'ADMIN')], default='user', verbose_name='Роль пользователя'),
        ),
    ]
