from django.db import models
from apps.accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    conditions = [
        ("New", "New"),
        ("Used", "Used"),
        ("Like New", "Like New")
    ]
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to='products/images', null=True, blank=True)
    condition = models.CharField(max_length=50, choices=conditions, default='New')
    views = models.ManyToManyField(User, related_name='views')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    posted_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-posted_date']
    def __str__(self): 
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images')

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.attribute} = {self.value}'
    
class Favorities(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, related_name='products')