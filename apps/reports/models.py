from django.db import models
from apps.accounts.models import User
from apps.products.models import Product
from django.utils import timezone, timesince
from datetime import timedelta

class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    reason = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="open")
    severity = models.CharField(max_length=50)

    def __str__(self):
        return self.reason

    @classmethod
    def get_recent_reports(cls):
        return cls.objects.filter(reported_at__gt=(timezone.now()-timedelta(days=7)))