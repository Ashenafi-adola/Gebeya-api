from rest_framework.serializers import ModelSerializer
from . models import Account, Address

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['username','first_name','last_name', 'avater', 'email', 'password']
        extra_kwargs = {'password':{'write_only': True}}

class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        extra_kwargs = {'user': {'read_only':True}}