from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer
from apps.products.models import Product, Category
from apps.products.serializers import ProductSerializer, CategorySerializer
from apps.reports.models import Report
from apps.reports.serializers import ReportSerializer
from rest_framework import generics
from rest_framework.views import View
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from datetime import timedelta
from django.utils import timezone

class AdminOverViewAPIView(generics.ListCreateAPIView):
    serializer_class  = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        users = User.objects.all().count()
        products = Product.objects.all().count()
        pending_product = Product.objects.filter(status="Pending").count()
        reports = Report.objects.all().count()

        return Response(
            {
                'users':users, 
                'products': products, 
                'pending': pending_product,
                'reports': reports
            }
        )

class GetReportsAPIView(generics.ListAPIView):
    serializer_class = ReportSerializer
    queryset = Report.get_recent_reports()
    permission_classes = [IsAdminUser]

