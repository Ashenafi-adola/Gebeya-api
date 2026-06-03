from django.urls import path
from . views import AddCategoryAPIView, AddProductAPIView, AddProductAttributeAPIView
from . import views
urlpatterns = [
    path('add-category/', AddCategoryAPIView.as_view(), name='add-category'),
    path('add-product/', AddProductAPIView.as_view(), name='add-product'),
    path('add-pro-attr/<int:pk>/', AddProductAttributeAPIView.as_view(), name='add-pro-attr'),
    path('categories/', views.CategoryListAPIView.as_view(), name='categories'),
    path('cate-products/<int:pk>/', views.CategoryProductListAPIView.as_view(), name='cate-products'),
    path('pro-detail/<int:pk>/', views.ProductDetailAPIView.as_view(), name='pro-detail')
]
