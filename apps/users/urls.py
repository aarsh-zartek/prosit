from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import DailyActivityView, UserViewSet, UserView


router = DefaultRouter()

router.register(prefix="user-update", viewset=UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("user/daily-activity", DailyActivityView.as_view(), name="user-daily-activity"),
    path("user", UserView.as_view(), name="user-details"),
]