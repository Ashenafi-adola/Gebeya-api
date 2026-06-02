from rest_framework.serializers import ModelSerializer
from . models import Category, Product, ProductAttribute

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {'seller':{'read_only': True}}

class ProductAttributeSerializer(ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['attribute', 'value', 'product']
