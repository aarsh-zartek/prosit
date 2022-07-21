from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.subscriptions.views import MySubscriptionView, UserSubscriptionViewSet


router = DefaultRouter()

router.register(
    prefix="subscriptions", viewset=UserSubscriptionViewSet, basename="subscriptions"
)

urlpatterns = [
    path("", include(router.urls)),
    path("my_subscription", MySubscriptionView.as_view(), name="my-subscription"),
]
