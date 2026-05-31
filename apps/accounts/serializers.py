from rest_framework.serializers import ModelSerializer
from . models import Account

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['username','first_name','last_name', 'avater', 'email', 'password']
        extra_kwargs = {'password':{'write_only': True}}