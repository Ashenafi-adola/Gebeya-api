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

class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if serializer.is_valid():
            instance = serializer.save()
            WishList.objects.create(user=instance)
            self.created_instance = instance
        else:
            pass
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        redirect_url = reverse(
            'add-address' 
        )
        return Response(
            status=status.HTTP_302_FOUND,
            headers={'Location': redirect_url}
        )

class UpdateUserAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
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