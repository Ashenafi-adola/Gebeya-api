from django.shortcuts import render, redirect
from rest_framework import generics
from . models import User, Address
from . serializers import UserSerializer, AddressSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, authenticate, logout
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from . import utilis
from apps.wishlist.models import WishList
from apps.products.models import Product, Favorities

class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if serializer.is_valid():
            instance = serializer.save()
            WishList.objects.create(user=instance)
            Favorities.objects.create(user=instance)
            self.created_instance = instance
            return Response(
                serializer.data
            )
        else:
            pass
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            serializer.data
        )

class UpdateUserAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

class GetProductSellerAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_object(self):
        return Product.objects.get(id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        user = self.get_object().seller
        serializer = UserSerializer(user)
        return Response(
            serializer.data,
        )
class GetAllUsersAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    
class GetUserAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serailizer = UserSerializer(user)
        return Response(serailizer.data)

class GetUserByIdAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    
class UpdateAddressAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

class AddAddressAPIView(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
       
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            print(serializer.data)
        else:
            pass