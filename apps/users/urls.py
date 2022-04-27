from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import UserView


router = DefaultRouter()


urlpatterns = [
    # path("", include(router.urls)),
    path("user", UserView.as_view(), name="user-details")
]