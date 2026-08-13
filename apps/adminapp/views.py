from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer
from apps.products.models import Product, Category
from apps.products.serializers import ProductSerializer, CategorySerializer
from apps.reports.models import Report
from apps.reports.serializers import ReportSerializer
from django.db.models import Count
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet


class AdminOverViewAPIView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        users = User.objects.aggregate(number=Count("id"))
        products = Product.objects.aggregate(number=Count("id"))
        pending_product = Product.objects.filter(status="Pending").count()
        reports = Report.objects.aggregate(number=Count("id"))

        return Response(
            {
                "users": users["number"],
                "products": products["number"],
                "pending": pending_product,
                "reports": reports["number"],
            }
        )

class GetRecentReportsAPIView(generics.ListAPIView):
    serializer_class = ReportSerializer
    queryset = Report.get_recent_reports()
    permission_classes = [IsAdminUser]

class ReportModerationAPIView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    def partial_update(self, request, *args, **kwargs):
        report = self.get_object()
        report.status = request.data["status"]
        report.save()
        return super().partial_update(request, *args, **kwargs)


class ManageUserAPIView(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        if "is_active" in request.data:
            user.is_active = request.data["is_active"]
        elif "is_superuser" in request.data:
            user.is_superuser = request.data["is_superuser"]
        user.save()
        return Response({"status": "success"})


class ManageProductAPIView(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()

    def partial_update(self, request, *args, **kwargs):
        product = self.get_object()
        try:
            if request.data["action"] == "accept":
                print(request.data)
                product.featured = "Featured"
                product.save()
                return Response({"response": "Featured"})

            elif request.data["action"] == "reject":
                product.featured = "NR"
                product.save()
                return Response({"response": "NR"})
        except KeyError:
            product.status = request.data["status"]
            product.save()
        return super().partial_update(request, *args, **kwargs)


class CategoryManagementAPIView(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
