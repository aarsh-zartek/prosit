from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.subscriptions.views import UserSubscriptionViewSet


router = DefaultRouter()

router.register(
    prefix="subscriptions", viewset=UserSubscriptionViewSet, basename="subscriptions"
)

urlpatterns = [
    path("", include(router.urls)),
]
