from django.db.models import Count
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Category, Product, ProductImage, Favorities


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "icon", "name", "description"]


class ProductSerializer(ModelSerializer):
    category = serializers.StringRelatedField()
    no_views = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "condition",
            "description",
            "no_views",
            "category",
            "views",
            "posted_date",
            "seller",
            "status",
            "featured",
        ]
        extra_kwargs = {
            "seller": {"read_only": True},
            "views": {"read_only": True},
            "status": {"read_only": True},
            "featured": {"read_only": True},
        }

    def get_no_views(self, obj):
        result = obj.views.aggregate(count=Count("id"))
        return result["count"]

    def get_seller(self, obj):
        user = obj.seller
        return user.first_name + " " + user.last_name


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"
        extra_kwargs = {"product": {"read_only"}}

    def create(self, validated_data):
        image = ProductImage.objects.create(**validated_data)
        return image

class FavoritiesSerializer(ModelSerializer):
    class Meta:
        model = Favorities
        fields = ["user", "product"]
        extra_kwargs = {"user": {"read_only": True}, "product": {"read_only": True}}
