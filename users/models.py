from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=255)
    expires_in = models.IntegerField(default=0)
    scope = models.CharField(max_length=255)

    bio = models.TextField(blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username