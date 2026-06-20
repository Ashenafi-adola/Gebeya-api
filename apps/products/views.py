from rest_framework import generics
from . serializers import ProductSerializer, CategorySerializer, ProductAttributeSerializer, ProductImageSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from . models import Product, ProductAttribute, Category, ProductImage
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

class RetriveUpdateDestroyCategoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
        
class AddProductAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_category(self):
        cat = self.request.data.get('category')
        try:
            return Category.objects.get(name=cat)
        except Exception:
            return None

    def perform_create(self, serializer):
        instance = serializer.save(seller=self.request.user)
        self.created_instance = instance

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        category = self.get_category()
        if category is None:
            return Response({'category': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        data['category'] = category.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AddProductImage(generics.CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RetriveUpdateDestroyProductAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        
        return super().get(request, *args, **kwargs)

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
    
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

class CategoryProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
