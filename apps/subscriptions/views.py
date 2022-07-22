from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.subscriptions.models import UserSubscription
from apps.subscriptions.serializers import (
    MySubscriptionSerializer,
    UserSubscriptionSerializer
)
from apps.subscriptions.services import RevenueCatService

from lib.constants import SubscriptionStatus

# Create your views here.


class UserSubscriptionViewSet(GenericViewSet, CreateModelMixin):
    queryset = UserSubscription.objects.select_related("user", "plan").all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=["post",], detail=False)
    def verify_purchase(self, request, *args, **kwargs):
        data = request.data
        product_identifier = data.get("product_identifier", None)
        rc_id = data.get("revenuecat_id", None)
        purchase_date = data.get("purchase_date", None)

        if not all([product_identifier, rc_id, purchase_date]):
            return Response(
                data={
                    "error": "All fields product_identifier, revenuecat_id, purchase_date must be provided"
                },
                status=HTTP_400_BAD_REQUEST,
            )

        rc = RevenueCatService(request.user.uid)
        verified = rc.verify_non_subscription_payment(
            product_identifier, rc_id, purchase_date
        )

        return Response(data={"purchase_verified": verified}, status=HTTP_200_OK)

    @action(methods=["patch",], detail=False)
    def revoke(self, request, *args, **kwargs) -> Response:
        """Revokes a user subscription by setting the 
        `subscription_status` to Cancelled
        """

        subscription = request.user.active_subscription
        if not subscription:
            return Response({
                    "message": "No Active Subscription found"
                }, status=HTTP_200_OK
            )
        subscription.subscription_status = SubscriptionStatus.CANCELLED
        subscription.save()
        
        return Response(data={
                "message": "Subscription Cancelled Successfully",
                "status": SubscriptionStatus.CANCELLED.capitalize()
            }, status=HTTP_200_OK
        )


class MySubscriptionView(APIView):

    serializer_class = MySubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        subscription = request.user.subscriptions.order_by('-created').first()
        if not subscription:
            return Response({
                    "message": "No Subscriptions found"
                }, status=HTTP_200_OK
            )
        serializer = self.serializer_class(instance=subscription)
        
        return Response(data=serializer.data, status=HTTP_200_OK)
