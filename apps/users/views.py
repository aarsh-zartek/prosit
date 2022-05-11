from django.http import JsonResponse

from rest_framework import mixins
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView

from apps.users.models import User, DailyActivity
from apps.users.serializers import UserSerializer, DailyActivitySerializer

# Create your views here.


class UserView(APIView):
	serializer_class = UserSerializer

	def get(self, request, *args, **kwargs):
		data = UserSerializer(instance=request.user).data
		return JsonResponse(data=data, status=HTTP_200_OK)


class UserViewSet(mixins.UpdateModelMixin, GenericViewSet):
	serializer_class = UserSerializer
	queryset = User.objects.all()
	
	def update(self, request, *args, **kwargs):
		serializer = UserSerializer(instance=request.user, data=request.data)
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
	