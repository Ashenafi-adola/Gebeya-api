import random
from django.core.mail import send_mail


def generate_otp():
    return random.randint(100000, 999999)


def send_email(email, otp):
    send_mail(
        "Email Verification",
        f"Your email verification OTP is {otp}",
        "astugebeysupport@gmail.com",
        [email],
        fail_silently=False,
    )
