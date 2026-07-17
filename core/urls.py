import re

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from rest_framework_simplejwt.views import TokenRefreshView

from core.views import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/health/", health_check, name="health-check"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Users: login + registration (token_obtain_pair lives here now)
    path("api/v1/", include("apps.users.urls")),
    path("api/v1/", include("apps.farmers.urls")),
    path("api/v1/", include("apps.products.urls")),
    path("api/v1/", include("apps.carts.urls")),
    path("api/v1/", include("apps.addresses.urls")),
    path("api/v1/", include("apps.orders.urls")),
]

# Serve uploaded media unconditionally (not just under DEBUG) — Django's
# static() shortcut is a no-op unless DEBUG=True, which would 404 every
# product image in production since there's no separate media server here.
urlpatterns += [
    re_path(
        r"^%s(?P<path>.*)$" % re.escape(settings.MEDIA_URL.lstrip("/")),
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]
