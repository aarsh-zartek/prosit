from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import CheckPhoneNumberExistsView, DailyActivityView, UserViewSet, UserView


router = DefaultRouter()

router.register(prefix="user-update", viewset=UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("user/daily-activity", DailyActivityView.as_view(), name="user-daily-activity"),
    path("user/check-phone-number", CheckPhoneNumberExistsView.as_view(), name="user-check-phone-number"),
    path("user", UserView.as_view(), name="user-details"),
]