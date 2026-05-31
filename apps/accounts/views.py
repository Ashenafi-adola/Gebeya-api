from django.shortcuts import render
from rest_framework import generics
from . models import Account, Address
from . serializers import AccountSerializer, AddressSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class CreateAccountAPIView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            pass

class AddAddressAPIView(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.user = self.request.user
            serializer.save()
        else:
            pass