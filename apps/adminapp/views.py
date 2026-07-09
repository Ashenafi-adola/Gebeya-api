from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer
from apps.products.models import Product, Category
from apps.products.serializers import ProductSerializer, CategorySerializer
from apps.reports.models import Report
from apps.reports.serializers import ReportSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ViewSet, ModelViewSet,ReadOnlyModelViewSet


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

class GetUsersAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

class ManageUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

    def get_user(self):
        return User.objects.get(id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        user = self.get_user()
        if request.data['action'] == 'status':
            user.is_active = request.data['data']
            user.save()
        elif request.data['action'] == 'promote':
            user.is_superuser = request.data['data']
            user.save()
        return Response({'status': 'success'})

class GetProductsAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()

class ManageProductAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()

    def get_product(self):
        return Product.objects.get(id=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        product = self.get_product()
        product.status = request.data['status']
        product.save()
        return Response(
            {
                'status':'success'
            }
        )

class CategoryManagementAPIView(ReadOnlyModelViewSet, generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()

class RetirieveUpdateDestroyCategoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

