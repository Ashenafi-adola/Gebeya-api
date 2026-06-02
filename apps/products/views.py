from rest_framework import generics
from . serializers import ProductSerializer, CategorySerializer, ProductAttributeSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from . models import Product, ProductAttribute, Category
from rest_framework.exceptions import PermissionDenied
from rest_framework.reverse import reverse
from rest_framework import  status
from rest_framework.response import Response   

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
        serializer.seller = self.request.user
        instance = serializer.save()
        self.created_instance = instance

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        redirect_url = reverse(
            f'add-pro-attr',
            kwargs={'pk':self.created_instance.id}
        )
        return Response(
            status= status.HTTP_302_FOUND,
            headers={'Location': redirect_url}
        )

class AddProductAttributeAPIView(generics.CreateAPIView):
    def get_queryset(self):
        ProductAttribute.objects.filter(product=self.get_object())
    
    def get_object(self):
        return Product.objects.get(id=self.kwargs['pk'])
    
    serializer_class = ProductAttributeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer): 
        instance = serializer.save(product = self.get_object())
        self.created_instance = instance

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        redirect_url = reverse(
            f'add-pro-attr',
            kwargs={'pk': self.get_object().id}
        )
        return Response(
            status= status.HTTP_302_FOUND,
            headers={'Location': redirect_url}
        )