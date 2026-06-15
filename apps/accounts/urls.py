from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CreateAccountAPIView.as_view(), name='register'),
    path('add-address/', views.AddAddressAPIView.as_view(), name='add-address'),
    path('update-account/', views.UpdateAccountAPIView.as_view()),
    path('update-address/', views.UpdateAddressAPIView.as_view())
]
