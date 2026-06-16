from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from . models import Account, Address
from django.contrib.auth import password_validation

class AccountSerializer(ModelSerializer):
    
    class Meta:
        model = Account
        fields = ['username','first_name','last_name', 'avater', 'email', 'password']
        extra_kwargs = {'password':{'write_only': True}}
    
    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user

class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        extra_kwargs = {'user': {'read_only':True}}