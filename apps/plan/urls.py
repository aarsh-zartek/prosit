from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.plan.views import DietPlanView, PlanCategoryView

router = DefaultRouter()

router.register(prefix="diet-plan", viewset=DietPlanView, basename="diet-plan")
router.register(prefix="plan-category", viewset=PlanCategoryView, basename="plan-category")

urlpatterns = [
	path("", include(router.urls)),
]