from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            return ValueError("Email field is required")
        
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(
            email,
            password,
            **extra_fields
        )

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username
    

class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    block_num = models.CharField(max_length=50)
    dorm_num = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)