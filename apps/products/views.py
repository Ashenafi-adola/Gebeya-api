from rest_framework import generics
from . serializers import ProductSerializer, CategorySerializer, ProductAttributeSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from . models import Product, ProductAttribute, Category
from rest_framework.exceptions import PermissionDenied

class AddCategoryAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            raise Exception("Exception occured while validating!")
        
class AddProductAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            raise Exception("Exception occured while validating!")

class AddProductAttributeAPIView(generics.CreateAPIView):
    def get_queryset(self):
        ProductAttribute.objects.filter(product=self.get_object())
    
    def get_object(self):
        return Product.objects.get(id=self.kwargs['pk'])
    
    serializer_class = ProductAttributeSerializer
    permission_classes = [IsAuthenticated]