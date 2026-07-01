from rest_framework import serializers
from . models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'reporter', 'product', 'reason', 'severity', 'status']
        extra_kwargs = {'reporter': {'read_only': True}, 'product':{'read_only':True}, 'status':{"read_only":True}}
        