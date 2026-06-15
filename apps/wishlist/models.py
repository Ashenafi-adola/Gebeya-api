from django.db import models
from apps.accounts.models import Account
from apps.products.models import Product

class WishList(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlists')