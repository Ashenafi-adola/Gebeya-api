from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User, Address, Contact
from apps.products.models import Product


class UserSerializer(ModelSerializer):
    listings = serializers.SerializerMethodField()

    class Meta:
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_superuser",
            "is_verified",
            "is_active",
            "listings",
        ]
        model = User
        extra_kwargs = {
            "password": {"write_only": True},
            "is_superuser": {"read_only": True},
            "is_verified": {"read_only": True},
            "is_active": {"read_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def get_listings(self, obj):
        return Product.objects.filter(seller=obj).count()


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}


class ContactSerializer(ModelSerializer):
    contacts = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = ["id", "user", "contacts"]
        extra_kwargs = {"user": {"read_only": True}}
