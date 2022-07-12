"""prosit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

router = DefaultRouter()

router.register("devices", FCMDeviceAuthorizedViewSet, basename="devices")


v1_url_patterns = [
    path("auth/", include("djoser.urls")),
    path("prosit/", include(("apps.about.urls", "about"), namespace="about")),
    path("user/", include(("apps.users.urls", "users"), namespace="users")),
    path("plan/", include(("apps.plan.urls", "plan"), namespace="plan")),
    path(
        "",
        include(("apps.notification.urls", "notification"), namespace="notification"),
    ),
    path("", include(router.urls)),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(v1_url_patterns))
]

schema_view = get_schema_view(
    openapi.Info(
        title="Swagger API",
        default_version="v1",
        description="Documentation for the Backend API",
    ),
    public=True,
)

urlpatterns += [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += [path("firebase/", include("apps.firebase.urls"))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
