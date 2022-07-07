from apps.core.serializers import DynamicFieldsModelSerializer
from apps.subscriptions.models import Subscription


class SubscriptionSerializer(DynamicFieldsModelSerializer):

	class Meta:
		model = Subscription
		fields = (
			"user", "plan", "amount_paid",
			"transaction_id", "payment_method", "payment_status",
			"subscription_status", "expires_on",
		)