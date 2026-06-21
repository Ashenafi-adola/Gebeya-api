from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CreateUserAPIView.as_view(), name='register'),
    path('add-address/', views.AddAddressAPIView.as_view(), name='add-address'),
    path('update-user/', views.UpdateUserAPIView.as_view()),
    path('update-address/', views.UpdateAddressAPIView.as_view()),
    path('get-user/<int:pk>/', views.GetProductSellerAPIView.as_view()),
    path('get-user/', views.GetUserAPIView.as_view())
]
