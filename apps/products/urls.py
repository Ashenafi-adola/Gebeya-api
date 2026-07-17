from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"myproducts", views.ManageMyProducts, basename="product")

urlpatterns = [
    path("categories/", views.CategoriesAPIView.as_view()),
    path("products/", views.GetAllProductsAPIView.as_view()),
    path("", include(router.urls)),
    path(
        "pro-detail/<int:pk>/", views.ProductDetailAPIView.as_view(), name="pro-detail"
    ),
    path("pro-fav/<int:pk>/", views.GetFavorities.as_view()),
    path("my-fav-products/", views.GetMyFavoriteProductsAPIView.as_view()),
    path("get-total-views/", views.GetMyTotalAPIView.as_view()),
]
