from rest_framework import generics
from .serializers import ProductSerializer, CategorySerializer, FavoritiesSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, Category, Favorities
from .paginators import CustomPageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from django.core.cache import cache


class CategoriesAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    queryset = Category.objects.all()


class GetAllProductsAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(status="Approved")
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination

    def paginate_queryset(self, queryset):
        return super().paginate_queryset(queryset)

    def get_queryset(self):
        qs = Product.objects.filter(status="Approved")
        if search := self.request.query_params.get("search"):
            qs = qs.filter(Q(name__icontains=search))

        if category := self.request.query_params.get("category"):
            cat = Category.objects.get(name=category)
            qs = qs.filter(category=cat.id)

        if condition := self.request.query_params.get("condition"):
            qs = qs.filter(condition=condition)

        if max_price := self.request.query_params.get("max_price"):
            qs = qs.filter(price__lte=max_price)

        if min_price := self.request.query_params.get("min_price"):
            qs = qs.filter(price__gte=min_price)

        return qs


class GetFeaturedProducts(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if fp := cache.get("fp"):
            return fp
        fp = Product.objects.filter(featured="Featured")
        cache.set("fp", fp, timeout=60 * 60 * 6)
        return fp


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

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

    def update(self, request, *args, **kwargs):
        p = self.get_object()
        if request.data["action"] == "fr-request":
            p.featured = "Pending"
            p.save()
            return Response({"response": "Pending"})

        return super().update(request, *args, **kwargs)


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

    def retrieve(self, request, *args, **kwargs):
        views = self.get_object().views.all()
        if self.request.user.id is not None:
            if self.request.user not in views:
                self.get_object().views.add(self.request.user)
        return super().retrieve(request, *args, **kwargs)


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
        if self.user_fav() is None:
            return Response("Not loged  in")
        serializer = FavoritiesSerializer(self.user_fav())
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        pro_id = self.kwargs["pk"]
        fav_pros = self.user_fav().product
        pro = Product.objects.get(id=pro_id)
        if self.user_fav() is None:
            return Response("No NO oops")

        if pro in fav_pros.all():
            fav_pros.remove(pro)
        else:
            fav_pros.add(pro)

        serializer = FavoritiesSerializer(self.user_fav())
        return Response(serializer.data)
