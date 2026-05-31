from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    avater = models.ImageField(upload_to='avater/')

    def __str__(self):
        return self.username
    
class Address(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    country = models.CharField(max_length=40)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)