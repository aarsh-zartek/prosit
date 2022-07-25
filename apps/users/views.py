from datetime import timedelta

from django.utils import timezone

from rest_framework import mixins
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from apps.users.filters import DailyActivityFilterSet
from apps.users.models import User, DailyActivity, UserHealthReport
from apps.users.serializers import DailyActivitySerializer, UserHealthReportSerializer, UserDietPlanSerializer


# Create your views here.


class UserPlanView(APIView):

	serializer_class = UserDietPlanSerializer
	permission_classes = (IsAuthenticated,)

	def get(self, request, *args, **kwargs):
		if request.user.active_subscription:
			if request.user.active_plan:
				serializer = self.serializer_class(
					instance=request.user, context={"request": self.request}
				)
				return Response(data=serializer.data, status=HTTP_200_OK)
			else:
				return Response({
						"message": "Your plan is being generated"
					}, status=HTTP_200_OK
				)
		else:
			return Response({
					"message": "No active subscription found"
				}, status=HTTP_200_OK
			)


class DailyActivityView(CreateAPIView, RetrieveAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = DailyActivitySerializer
	filter_backends = (DjangoFilterBackend,)
	filterset_class = DailyActivityFilterSet
	
	def get_queryset(self):
		return DailyActivity.objects.filter(user=self.request.user).order_by('date')
	
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=HTTP_201_CREATED)
	
	def retrieve(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())
		serializer = self.get_serializer(queryset, many=True, exclude=["user"])
		return Response({
				"activity_data": serializer.data,
				"diet_plan_active": True if request.user.active_plan else False
			}, status=HTTP_200_OK
		)


class UserHealthReportViewSet(mixins.CreateModelMixin, GenericViewSet):
	serializer_class = UserHealthReportSerializer
	permission_classes = (IsAuthenticated,)

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['user'] = self.request.user
		return context

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=HTTP_201_CREATED)


class CheckPhoneNumberExistsView(APIView):
	
	permission_classes = (AllowAny,)
	def post(self, request):
		phone_number = request.data.get('phone_number')

		if not phone_number:
			return Response(data={
				'error': 'Please provide a phone number'
			}, status=HTTP_422_UNPROCESSABLE_ENTITY
		)
		exists = User.objects.filter(phone_number=phone_number).exists()
		return Response(
			data={
				"success": exists
			}, status=HTTP_200_OK
		)


class CheckHealthReportExistsView(APIView):
	permission_classes = (IsAuthenticated,)
	
	def get(self, request):
		uploaded = UserHealthReport.objects.filter(
				user=request.user,
				date__gte=timezone.now() - timedelta(days=7)
			).exists()

		return Response({
			"health_reports_uploaded": uploaded
		}, status=HTTP_200_OK)
