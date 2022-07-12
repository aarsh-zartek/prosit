from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.notification.views import UserNotificationViewSet

router = DefaultRouter()


router.register(
    prefix="notification",
    viewset=UserNotificationViewSet,
    basename="user-notifications",
)

urlpatterns = [
    path("", include(router.urls)),
]
