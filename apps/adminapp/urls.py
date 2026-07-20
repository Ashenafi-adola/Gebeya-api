from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"reports", views.ReportModerationAPIView, basename="report")
router.register(r"products", views.ManageProductAPIView, basename="product")
router.register(r"categories", views.CategoryManagementAPIView, basename="category")
router.register(r"users", views.ManageUserAPIView, basename="user")

urlpatterns = [
    path("overview/", views.AdminOverViewAPIView.as_view()),
    path("recent-reports/", views.GetRecentReportsAPIView.as_view()),
    path("", include(router.urls)),
]
