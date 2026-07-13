from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", views.ManageUserAPIVew, basename="user")

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterUserAPIView.as_view()),
    path('get-user/<int:pk>/', views.GetProductSellerAPIView.as_view()),
    path("get-user-by-email/<str:email>/", views.GetUserByEmail.as_view()),
    path('get-my-contacts/', views.GetMyContacts.as_view()),
    path('verify-email/<str:email>/', views.VerifyEmailAPIView.as_view())
]
