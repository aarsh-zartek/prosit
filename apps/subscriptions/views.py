from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.subscriptions.models import Subscription
from apps.subscriptions.serializers import SubscriptionSerializer

# Create your views here.


class SubscriptionViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
):

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class CheckPaymentStatus(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        user = request.user
        subscriptions = user.subscriptions.all()
        return Response({"payment_status": "0"}, status=HTTP_200_OK)
