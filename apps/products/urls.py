from django.urls import path
from . import views
urlpatterns = [
    path('categories/', views.CategoriesAPIView.as_view()),
    path('products/', views.GetAllProductsAPIView.as_view()),
    path('products/new/', views.AddProductAPIView.as_view()),
    path('products-image/<int:pk>/', views.AddProductImage.as_view()),
    path("product-detail/<int:pk>/", views.RetriveUpdateDestroyProductAPIView.as_view()),
    path('categories/', views.CategoryListAPIView.as_view(), name='categories'),
    path('retrive-cate/<int:pk>/', views.RetriveUpdateDestroyCategoryAPIView.as_view()),
    path('cate-products/<int:pk>/', views.CategoryProductListAPIView.as_view(), name='cate-products'),
    path('pro-detail/<int:pk>/', views.ProductDetailAPIView.as_view(), name='pro-detail'),
    path('pro-fav/<int:pk>/', views.GetFavorities.as_view()),
    path('my-pros/', views.GetMyProductsAPIView.as_view()),
    path('my-fav-products/', views.GetMyFavoriteProductsAPIView.as_view()),
    path('get-total-views/', views.GetMyTotalAPIView.as_view()),
]
