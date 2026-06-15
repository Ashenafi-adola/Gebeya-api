from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    avater = models.ImageField(upload_to='avater/')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    

class OTPVerification(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Address(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    block_num = models.CharField(max_length=50)
    dorm_num = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)