from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.AdminOverViewAPIView.as_view()),
    path('reports/', views.GetReportsAPIView.as_view()),
    path('users/', views.GetUsersAPIView.as_view()),
    path('manage-user/<int:pk>/', views.ManageUserAPIView.as_view()),
    path('products/', views.GetProductsAPIView.as_view()),
    path('manage-product/<int:pk>/', views.ManageProductAPIView.as_view()),
    path('manage-category/', views.CategoryManagementAPIView.as_view({'get': 'list'})),
    path('category/<int:pk>/', views.RetirieveUpdateDestroyCategoryAPIView.as_view()),
]
