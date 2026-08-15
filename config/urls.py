from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny


class PublicTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]


class PublicTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


urlpatterns = [
    path("admin/main/", admin.site.urls),
    path("admin/", include("apps.adminapp.urls")),
    path("api/accounts/", include("apps.accounts.urls")),
    path("products/", include("apps.products.urls")),
    path("reports/", include("apps.reports.urls")),
    path("chat/", include("apps.chat.urls")),
    path("wishlist/", include("apps.wishlist.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", PublicTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", PublicTokenRefreshView.as_view(), name="token_refresh"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
