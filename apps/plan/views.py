from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from apps.plan.serializers import DietPlanSerializer, DietPlanListSerializer, PlanCategorySerializer
from apps.plan.models import DietPlan, PlanCategory
from apps.core.mixins import SerializerActionClassMixin

from lib.choices import PLAN_TYPES

# Create your views here.


class DietPlanView(
	SerializerActionClassMixin,
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	GenericViewSet
):
	serializer_class = DietPlanSerializer
	serializer_action_classes = {
		'list': DietPlanListSerializer,
		'retrieve': DietPlanSerializer
	}
	permission_classes = (AllowAny,)

	def get_queryset(self):
		
		queryset = DietPlan.objects
		if self.action == 'list':
			queryset = queryset.filter(plan_type=PLAN_TYPES.main_category)
		else:
			queryset = queryset.all()
		
		return queryset

class PlanCategoryView(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
	serializer_class = PlanCategorySerializer
	queryset = PlanCategory.objects.all()
	permission_classes = (AllowAny,)

