from django.urls import path
from . views import CreateAccountAPIView, AddAddressAPIView

urlpatterns = [
    path('register/', CreateAccountAPIView.as_view(), name='register'),
    path('add-address/', AddAddressAPIView.as_view(), name='add-address'),
]
