from django.urls import path
from . import views

urlpatterns = [path("messages/<int:pk>/", views.MessageListAPIView.as_view())]
