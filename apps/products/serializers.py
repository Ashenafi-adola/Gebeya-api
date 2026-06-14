from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from . models import Category, Product, ProductAttribute, ProductImage

class CategorySerializer(ModelSerializer):
    name = HyperlinkedIdentityField(
        view_name='cate-products',
        lookup_field='pk'
    )
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductSerializer(ModelSerializer):
    name = HyperlinkedIdentityField(
        view_name='pro-detail',
        lookup_field='pk'
    ) 
    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {'seller':{'read_only': True}}

class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        extra_kwargs = {'product':{'read_only'}}

class ProductAttributeSerializer(ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['attribute', 'value', 'product']
