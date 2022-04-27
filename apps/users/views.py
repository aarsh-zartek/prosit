from django.http import JsonResponse

from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.serializers import UserSerializer

# Create your views here.


class UserView(APIView):

	def get(self, request, *args, **kwargs):
		data = UserSerializer(instance=request.user).data
		return JsonResponse(data=data, status=HTTP_200_OK)