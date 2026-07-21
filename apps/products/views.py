from rest_framework import generics
from .serializers import ProductSerializer, CategorySerializer, FavoritiesSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, Category, Favorities
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.core.cache import cache


class CategoriesAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    queryset = Category.objects.all()


class GetAllProductsAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(status="Approved")
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        products = cache.get("products")
        
        if not products:
            products = Product.objects.filter(status="Approved")
            cache.set("products", products, timeout=60*30)
            return products
        
        return products


class ManageMyProducts(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_category(self, cat):
        try:
            return Category.objects.get(name=cat)
        except Exception:
            return None

    def perform_create(self, serializer):
        instance = serializer.save(
            seller=self.request.user,
            category=self.get_category(self.request.data["category"]),
        )
        self.created_instance = instance

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        cate = self.get_category(data["category"])
        data["category"] = cate.id
        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        views = self.get_object().views.all()
        if self.request.user.id is not None:
            if self.request.user not in views:
                self.get_object().views.add(self.request.user)
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)


class GetMyFavoriteProductsAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        fav = Favorities.objects.get(user=self.request.user)
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

        res = {"total_views": total_views}
        return Response(res)


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
            return Favorities.objects.create(user=self.request.user)

    def get(self, request, *args, **kwargs):
        if self.user_fav() == None:
            return Response("Not loged  in")
        serializer = FavoritiesSerializer(self.user_fav())
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        pro_id = self.kwargs["pk"]
        fav_pros = self.user_fav().product
        pro = Product.objects.get(id=pro_id)
        if self.user_fav() == None:
            return Response("No NO oops")

        if pro in fav_pros.all():
            fav_pros.remove(pro)
        else:
            fav_pros.add(pro)

        serializer = FavoritiesSerializer(self.user_fav())
        return Response(serializer.data)
