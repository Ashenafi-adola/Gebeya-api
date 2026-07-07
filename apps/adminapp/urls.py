from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.AdminOverViewAPIView.as_view()),
    path('reports/', views.GetReportsAPIView.as_view())
]
