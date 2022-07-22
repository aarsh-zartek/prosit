from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from apps.about.models import FAQ, Company
from apps.about.serializers import CompanySerializer, ContactFormSerializer, FAQSerializer

# Create your views here.


class CompanyView(APIView):
	
	permission_classes = (AllowAny,)
	def get(self, request, *args, **kwargs):
		instance = Company.objects.first()
		serializer = CompanySerializer(instance)
		return Response(serializer.data, status=HTTP_200_OK)

class FAQView(ListAPIView):
	queryset = FAQ.objects.all()
	serializer_class = FAQSerializer
	
	permission_classes = (AllowAny,)


class ContactFormView(CreateAPIView):

	permission_classes = (IsAuthenticated,)
	serializer_class = ContactFormSerializer
	throttle_scope = "contact_form"
