from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from apps.subscriptions.models import UserSubscription
from apps.subscriptions.serializers import UserSubscriptionSerializer
from apps.subscriptions.services import RevenueCatService

# Create your views here.


class UserSubscriptionViewSet(GenericViewSet, CreateModelMixin):
    queryset = UserSubscription.objects.select_related("user", "plan").all()
    serializer_class = UserSubscriptionSerializer

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
