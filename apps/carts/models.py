from django.db import models
from accounts.models import Account
from products.models import Product

class Cart(models.Model):
    owner = models.OneToOneField(Account, on_delete=models.CASCADE)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    