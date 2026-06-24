from rest_framework import generics, views, viewsets
from . serializers import ProductSerializer, CategorySerializer, ProductAttributeSerializer, ProductImageSerializer, FavoritiesSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from . models import Product, ProductAttribute, Category, ProductImage, Favorities
from rest_framework.exceptions import PermissionDenied
from rest_framework.reverse import reverse
from rest_framework import  status
from rest_framework.response import Response   
from rest_framework.views import APIView

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

    
class GetAllProductsAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
        
class AddProductAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_category(self, cat):
        try:
            return Category.objects.get(name=cat)
        except Exception:
            return None

    def perform_create(self, serializer):
        instance = serializer.save(seller=self.request.user,category=self.get_category(self.request.data['category']))
        self.created_instance = instance

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        cate = self.get_category(data['category'])
        data['category'] = cate.id
        print(data)
        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data
        )


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

    def get_product(self):
        return Product.objects.get(id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        views = self.get_product().views.all()
        if self.request.user.id is not None:
            if self.request.user not in views:
                self.get_product().views.add(self.request.user)
        return super().get(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class GetMyProductsAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(seller= self.request.user)
    
class GetMyFavoriteProductsAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        fav = Favorities.objects.get(user= self.request.user)
        fav_products = fav.product.all()
        return fav_products

class GetMyTotalAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

    def get(self, request, *args, **kwargs):
        total_views = 0
        for i in self.get_queryset():
            total_views += i.views.all().count()

        res = {
            'total_views':total_views
        }
        return Response(res)
    
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

class GetFavorities(generics.RetrieveAPIView):
    queryset = Favorities.objects.all()
    serializer_class = FavoritiesSerializer
    permission_classes = [IsAuthenticated]

    def user_fav(self):
        try:
            return Favorities.objects.get(user=self.request.user)
        except Favorities.DoesNotExist:
            return None
    def get(self, request, *args, **kwargs):
        if self.user_fav() == None:
            return Response("Not loged  in")
        serializer = FavoritiesSerializer(self.user_fav())
        return Response(
            serializer.data
        )

    def post(self, request, *args, **kwargs):
        pro_id = self.kwargs['pk']
        fav_pros = self.user_fav().product
        pro = Product.objects.get(id=pro_id)
        if self.user_fav() == None:
            return Response("No NO oops")
        
        if pro in fav_pros.all():
            fav_pros.remove(pro)
        else:
            fav_pros.add(pro)

        serializer = FavoritiesSerializer(self.user_fav())
        return Response(
            serializer.data
        )
        
