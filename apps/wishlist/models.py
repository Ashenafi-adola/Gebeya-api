from django.db import models
from apps.accounts.models import User
from apps.products.models import Product


class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name="wishlists")
