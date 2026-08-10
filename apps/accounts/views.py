from rest_framework import generics
from .models import User, Contact, OTPVerification
from .serializers import UserSerializer, ContactSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .utilis import generate_otp, send_email
from apps.wishlist.models import WishList
from apps.products.models import Product, Favorities
from rest_framework.viewsets import ModelViewSet


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
        instance = serializer.save()
        otp_code = generate_otp()
        OTPVerification.objects.create(user=instance, otp=otp_code)
        send_email(instance.email, otp_code)
        WishList.objects.create(user=instance)
        Favorities.objects.create(user=instance)
        self.created_instance = instance
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)


class VerifyEmailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User
    lookup_field = "email"

    def get_object(self):
        return User.objects.get(email=self.kwargs["email"])

    def post(self, request, *args, **kwargs):
        user = User.objects.get(email=self.kwargs["email"])
        OTP = OTPVerification.objects.get(user=self.get_object())
        if OTP.is_expired():
            otp_code = generate_otp()
            OTP.otp = otp_code
            OTP.save()
            send_email(request.data["email"], otp_code)
            return Response({"message": "OTP expired", "is_verified": user.is_verified})
        else:
            if request.data["otp"] == OTP.otp:
                user.is_verified = True
                user.save()
                return Response(
                    {"message": "Successfull verifyed", "is_verified": user.is_verified}
                )
            else:
                return Response(
                    {"message": "Incorrenct OTP code!", "is_verified": user.is_verified}
                )


class GetProductSellerAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_object(self):
        return Product.objects.get(id=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        user = self.get_object().seller
        serializer = UserSerializer(user)
        return Response(
            serializer.data,
        )


class GetUserByEmail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def get_object(self):
        return User.objects.get(email=self.kwargs["email"])


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
