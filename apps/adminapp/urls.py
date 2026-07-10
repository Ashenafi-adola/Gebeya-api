from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"reports", views.ReportModerationAPIView, basename='report')
router.register(r"products", views.ManageProductAPIView, basename='product')
router.register(r"categories", views.CategoryManagementAPIView, basename='category')

urlpatterns = [
    path('overview/', views.AdminOverViewAPIView.as_view()),
    path('recent-reports/', views.GetRecentReportsAPIView.as_view()),
    path('', include(router.urls)),
    path('users/', views.GetUsersAPIView.as_view()),
    path('manage-user/<int:pk>/', views.ManageUserAPIView.as_view()),
]

