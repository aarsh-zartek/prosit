from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import CheckPhoneNumberExistsView, DailyActivityView, UserHealthReportViewSet, CheckHealthReportExistsView, UserPlanView


router = DefaultRouter()

router.register(prefix="health-report", viewset=UserHealthReportViewSet, basename="user-health-report")

urlpatterns = [
    path("", include(router.urls)),
    path("daily-activity", DailyActivityView.as_view(), name="user-daily-activity"),
    path("check-health-report", CheckHealthReportExistsView.as_view(), name="user-check-health-report"),
    path("check-phone-number", CheckPhoneNumberExistsView.as_view(), name="user-check-phone-number"),
    path("my-plan", UserPlanView.as_view(), name="user-plan"),
]