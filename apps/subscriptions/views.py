from rest_framework.mixins import (
    CreateModelMixin,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.subscriptions.models import UserSubscription
from apps.subscriptions.serializers import (
    VerifyPurchaseSerializer,
    UserSubscriptionSerializer,
)

# # Create your views here.


class UserSubscriptionViewSet(GenericViewSet, CreateModelMixin):
    queryset = UserSubscription.objects.select_related("user", "plan").all()
    serializer_class = UserSubscriptionSerializer


# class CheckPaymentStatus(APIView):
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         subscriptions = user.subscriptions.all()
#         return Response({"payment_status": "0"}, status=HTTP_200_OK)


# class VerifyPurchaseView(APIView):
#     serializer_class = VerifyPurchaseSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(request.data)

#         return Response({"data": serializer.data}, status=HTTP_200_OK)


"""
Response
D/[Purchases] - DEBUG(31146): :information_source: BillingWrapper purchases updated: skus: [smart_plan_199], orderId: GPA.3305-0609-9204-98023, purchaseToken: dnjgdllkapjbakjacapncjgj.AO-J1OxmqlbeTMbyeIjblFVEvkG6hsm3kI_b4D6uIVAkan-mIzNweNThoek7DgdZH20duN_S6WWK_qptBFbwAVLaxhx7Q-o62g
"""
