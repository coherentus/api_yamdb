# Generated by Django 2.2.16 on 2021-10-26 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210816_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Администратор'), ('user', 'Аутентифицированный пользователь'), ('moderator', 'Модератор')], default='user', max_length=20, verbose_name='Роль'),
        ),
    ]
