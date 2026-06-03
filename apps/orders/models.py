from django.db import models
from products.models import Product
from accounts.models import Account


class Order(models.Model):
    PENDING = 'P'
    COMPLETE = "C"
    FAILED = 'F'

    PAYMENT_STATUS = [
        (PENDING,'pending'),
        (COMPLETE,'complete'),
        (FAILED,'faild'),
    ]
    Placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PENDING)
    buyer = models.ForeignKey(Account, on_delete=models.CASCADE)
   
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    