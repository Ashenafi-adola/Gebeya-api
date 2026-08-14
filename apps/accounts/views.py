from .models import User, Contact, OTPVerification
from .serializers import UserSerializer, ContactSerializer
from .utilis import generate_otp, send_email
from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.wishlist.models import WishList
from apps.products.models import Product, Favorities


class ManageUserAPIVew(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            User.objects.all()
            .exclude(id=self.request.user.id)
            .exclude(is_superuser=True)
        )

    def get_object(self):
        user = User.objects.get(id=self.kwargs["pk"])
        if user == self.request.user:
            return user
        return super().get_object()


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        with transaction.atomic():
            instance = serializer.save()
            otp_code = generate_otp()
            otp = OTPVerification(user=instance)
            otp.set_opt(otp_code)
            Favorities.objects.create(user=instance)
            send_email(instance.email, otp_code)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)


class VerifyEmailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    lookup_field = "email"

    def post(self, request, *args, **kwargs):
        OTP = OTPVerification.objects.get(user=self.get_object())
        if OTP.verify_otp(request.data["otp"]):
            return Response(
                {"message": "Successfull verifyed", "is_verified": self.get_object().is_verified}
            )
        else:
            if not OTP.is_active:
                return Response(
                    {"message": "Too many trials", "is_verified": self.get_object().is_verified}
                )
            elif OTP.is_expired():
                return Response(
                    {"message": "Your OTP is expired click resend for new OTP", "is_verified": self.get_object().is_verified}
                )
            else:
                return Response(
                    {"message": "Incorrect", "is_verified": self.get_object().is_verified}
                )


class GetProductSellerAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_object(self):
        return Product.objects.get(id=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(self.get_object().seller)
        return Response(
            serializer.data,
        )


class GetUserByEmail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    lookup_field = "email"

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
