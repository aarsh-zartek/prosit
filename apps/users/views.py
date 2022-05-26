from django.http import JsonResponse

from rest_framework import mixins
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView

from apps.users.models import User, DailyActivity
from apps.users.serializers import UserSerializer, DailyActivitySerializer, UserHealthReportSerializer

# Create your views here.


class UserView(APIView):
	serializer_class = UserSerializer
	permission_classes = (IsAuthenticated,)

	def get(self, request, *args, **kwargs):
		data = self.serializer_class(instance=request.user).data
		return JsonResponse(data=data, status=HTTP_200_OK)


class UserViewSet(mixins.UpdateModelMixin, GenericViewSet):
	serializer_class = UserSerializer
	permission_classes = (IsAuthenticated,)
	queryset = User.objects.prefetch_related('profile').all()
	
	def update(self, request, *args, **kwargs):
		serializer = self.serializer_class(instance=request.user, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return JsonResponse(
			data={
				"data": serializer.data,
			}, status=HTTP_202_ACCEPTED
		)


class DailyActivityView(CreateAPIView):
	serializer_class = DailyActivitySerializer
	permission_classes = (IsAuthenticated,)
	
	def get_queryset(self):
		return DailyActivity.objects.filter(user=self.request.user)


class UserHealthReportViewSet(mixins.CreateModelMixin, GenericViewSet):
	serializer_class = UserHealthReportSerializer
	permission_classes = (IsAuthenticated,)

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['user'] = self.request.user
		return context


class CheckPhoneNumberExistsView(APIView):
	
	permission_classes = (AllowAny,)
	def post(self, request):
		phone_number = request.data.get('phone_number')

		if not phone_number:
			return JsonResponse(data={
				'error': 'Please provide a phone number'
			}, status=HTTP_422_UNPROCESSABLE_ENTITY
		)
		exists = User.objects.filter(phone_number=phone_number).exists()
		return JsonResponse(
			data={
				"success": exists
			}, status=HTTP_200_OK
		)
