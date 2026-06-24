from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from . models import User, Address
from django.contrib.auth import password_validation

class UserSerializer(ModelSerializer):
    class Meta:
        fields = ['id','first_name','last_name', 'email', 'password']
        model = User
        extra_kwargs = {'password':{'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        extra_kwargs = {'user': {'read_only':True}}