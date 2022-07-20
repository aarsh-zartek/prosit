from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.plan.views import DietPlanView

router = DefaultRouter()

router.register(prefix="diet-plan", viewset=DietPlanView, basename="diet-plan")

urlpatterns = [
	path("", include(router.urls)),
]
