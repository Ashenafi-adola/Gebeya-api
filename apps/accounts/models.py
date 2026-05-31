from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    avater = models.ImageField(upload_to='avater/')
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.username