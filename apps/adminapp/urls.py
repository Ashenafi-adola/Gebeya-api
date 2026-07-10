from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"reports", views.ReportModerationAPIView, basename='report')

urlpatterns = [
    path('overview/', views.AdminOverViewAPIView.as_view()),
    path('recent-reports/', views.GetRecentReportsAPIView.as_view()),
    path('', include(router.urls)),
    path('users/', views.GetUsersAPIView.as_view()),
    path('manage-user/<int:pk>/', views.ManageUserAPIView.as_view()),
    path('products/', views.GetProductsAPIView.as_view()),
    path('manage-product/<int:pk>/', views.ManageProductAPIView.as_view()),
    path('manage-category/', views.CategoryManagementAPIView.as_view({'get': 'list'})),
    path('category/<int:pk>/', views.RetirieveUpdateDestroyCategoryAPIView.as_view()),
]

