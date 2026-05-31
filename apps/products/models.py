from django.db import models
from accounts.models import Account

class Category(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/images/')

    def __str__(self):
        return self.name

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.attribute} = {self.value}'