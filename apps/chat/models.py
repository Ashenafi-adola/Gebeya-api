from django.db import models
from apps.accounts.models import Account


class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="senders")
    reciever = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name="recievers")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    