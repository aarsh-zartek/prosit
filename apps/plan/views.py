from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.plan.serializers import DietPlanSerializer, DietPlanListSerializer, PlanCategorySerializer
from apps.plan.models import DietPlan, PlanCategory
from apps.core.mixins import SerializerActionClassMixin

from lib.choices import PLAN_TYPES

# Create your views here.


class DietPlanView(SerializerActionClassMixin, ReadOnlyModelViewSet):
	queryset = DietPlan.objects.all()
	serializer_class = DietPlanSerializer
	serializer_action_classes = {
		'list': DietPlanListSerializer,
		'retrieve': DietPlanSerializer
	}
	permission_classes = (AllowAny,)

	def get_queryset(self):
		queryset = self.queryset
		if self.action == 'list':
			queryset = queryset.filter(plan_type=PLAN_TYPES.main_category)
		return queryset

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context["user"] = self.request.user
		return context
