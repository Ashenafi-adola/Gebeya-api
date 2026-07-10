from rest_framework import serializers
from . models import Report


class ReportSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    product_id = serializers.SerializerMethodField()
    reporter = serializers.StringRelatedField()
    class Meta:
        model = Report
        fields = ['id', 'reporter', 'product', 'product_id', 'reason', 'severity', 'status']
        extra_kwargs = {'reporter': {'read_only': True}, 'product':{'read_only':True}, 'status':{"read_only":True}}
    
    def get_product_id(self, obj):
        return obj.product.id
