from django.contrib.auth.models import AbstractUser
from django.db import models

CHOISES = (('admin', 'Администратор'),
           ('user', 'Аутентифицированный пользователь'),
           ('moderator', 'Модератор'),
           ('anon', 'Аноним'),
           ('superuser', 'Суперюзер Django'))


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField('Роль', max_length=20,
                            choices=CHOISES, default='user')
