from django.urls import path
from . views import AddCategoryAPIView, AddProductAPIView, AddProductAttributeAPIView

urlpatterns = [
    path('add-category/', AddCategoryAPIView.as_view(), name='add-category'),
    path('add-product/', AddProductAPIView.as_view(), name='add-product'),
    path('add-product-attr/', AddProductAttributeAPIView.as_view(), name='add-pro-attr')
]
