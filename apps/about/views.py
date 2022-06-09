from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from apps.about.models import Company
from apps.about.serializers import CompanySerializer

# Create your views here.


class CompanyView(APIView):
	
	permission_classes = (AllowAny,)
	def get(self, request, *args, **kwargs):
		instance = Company.objects.first()
		serializer = CompanySerializer(instance)
		return Response(serializer.data, status=HTTP_200_OK)