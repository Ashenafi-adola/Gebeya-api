from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from . models import Category, Product, ProductAttribute, ProductImage
from rest_framework import serializers

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'condition', 'description', 'category']
        extra_kwargs = {'seller':{'read_only': True}}

class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        extra_kwargs = {'product':{'read_only'}}
    
    def create(self, validated_data):
        image = ProductImage.objects.create(**validated_data)
        return image

class ProductAttributeSerializer(ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['attribute', 'value', 'product']
