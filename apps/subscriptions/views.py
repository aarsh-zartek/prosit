from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.subscriptions.models import Subscription
from apps.subscriptions.serializers import SubscriptionSerializer

# Create your views here.


class SubscriptionViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):

	queryset = Subscription.objects.all()
	serializer_class = SubscriptionSerializer