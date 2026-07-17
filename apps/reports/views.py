from rest_framework import generics
from .models import Report
from apps.products.models import Product
from .serializers import ReportSerializer
from rest_framework.permissions import IsAuthenticated


class CreateReportAPIView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.kwargs["pk"])
        if serializer.is_valid():
            serializer.save(reporter=self.request.user, product=product)
