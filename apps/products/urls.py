from django.urls import path
from . import views
urlpatterns = [
    path('add-category/', views.AddCategoryAPIView.as_view(), name='add-category'),
    path('add-product/', views.AddProductAPIView.as_view(), name='add-product'),
    path('add-pro-attr/<int:pk>/', views.AddProductAttributeAPIView.as_view(), name='add-pro-attr'),
    path('categories/', views.CategoryListAPIView.as_view(), name='categories'),
    path('retrive-cate/<int:pk>/', views.RetriveUpdateDestroyCategoryAPIView.as_view()),
    path('cate-products/<int:pk>/', views.CategoryProductListAPIView.as_view(), name='cate-products'),
    path('pro-detail/<int:pk>/', views.ProductDetailAPIView.as_view(), name='pro-detail')
]
