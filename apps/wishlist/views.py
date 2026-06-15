from rest_framework import generics
from rest_framework import views, viewsets
from . models import WishList
from apps.products.models import Product
from apps.accounts.models import Account
from rest_framework.permissions import IsAuthenticated
from . serializers import WishListSerializer

class AddProductToWishListAPIView(generics.UpdateAPIView):
    permission_classes = IsAuthenticated
    serializer_class = WishListSerializer
    queryset = WishList.objects.all()

    def get_object(self):
        return WishList.objects.get(user=self.request.user)
    
    def patch(self, request, *args, **kwargs):
        wishlistProducts = self.get_object().products
        product = Product.objects.get(id=self.kwargs['pk'])

        if product not in wishlistProducts:
            wishlistProducts.add(product)
        else:
            wishlistProducts.remove(product)