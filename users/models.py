from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=False)
    email = models.EmailField(unique=True)
    tg_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='id в Телеграм')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = [
            "email",
        ]
        db_table = 'users'
