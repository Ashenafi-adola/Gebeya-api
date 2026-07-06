from django.shortcuts import render, redirect
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from . models import User, Address, Contact, OTPVerification
from . serializers import UserSerializer, AddressSerializer, ContactSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, authenticate, logout
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .utilis import generate_otp, send_email
from apps.wishlist.models import WishList
from apps.products.models import Product, Favorities


class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if serializer.is_valid():
            instance = serializer.save()
            otp_code = generate_otp()
            user_otp = OTPVerification.objects.create(user=instance, otp=otp_code)
            send_email(instance.email, otp_code)
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

class VerifyEmailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User
    lookup_field = 'email'

    def get_object(self):
        return User.objects.get(email=self.kwargs['email']) 

    def post(self, request, *args, **kwargs):
        print(request.data)
        user = User.objects.get(email=self.kwargs['email'])
        OTP = OTPVerification.objects.get(user=self.get_object())
        if OTP.is_expired():
            otp_code = generate_otp()
            OTP.otp = otp_code
            OTP.save()
            send_email(request.data['email'], otp_code)
            return Response({'message': 'OTP expired', 'is_verified': user.is_verified})
        else:
            if request.data['otp'] == OTP.otp:
                user.is_verified = True
                user.save()
                return Response({"message": "Successfull verifyed", 'is_verified': user.is_verified})
            else:
                return Response({"message": "Incorrenct OTP code!", 'is_verified': user.is_verified})

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
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all().exclude(id=self.request.user.id).exclude(is_superuser=True)
    
class GetUserByEmail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def get_object(self):
        return User.objects.get(email=self.kwargs['email'])


    
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

class GetMyContacts(generics.RetrieveAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    queryset = Contact.objects.all()

    def get_object(self):
        try:
            return Contact.objects.get(user=self.request.user)
        except Exception:
            cont = Contact.objects.create(user=self.request.user)
            return cont

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