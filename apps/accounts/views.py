from django.shortcuts import render, redirect
from rest_framework import generics
from . models import Account, Address
from . serializers import AccountSerializer, AddressSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, authenticate, logout
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from . import utilis

class CreateAccountAPIView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if serializer.is_valid():
            instance = serializer.save()
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