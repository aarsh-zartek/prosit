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
from django.contrib import admin
from django.urls import include, path

from djoser.views import TokenCreateView, TokenDestroyView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api/', include("djoser.urls.jwt")),
    # path('api/', include('rest_framework.urls')),
    
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    
    path('login/', TokenCreateView.as_view(), name='login'),
    path('logout/', TokenDestroyView.as_view(), name='logout'),
    
    path("firebase/", include("apps.firebase.urls")),
        
    path("api/v1/", include(("apps.users.urls", "users"), namespace="users")),
    path("api/v1/", include(("apps.plan.urls", "plan"), namespace="plan")),
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
            name="schema-swagger-ui"),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        )]
