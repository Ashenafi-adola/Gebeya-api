from rest_framework import serializers
from .models import WishList


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = "__all__"
        extra_kwargs = {"user": {"write_only": True}}
