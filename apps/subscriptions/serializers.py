from rest_framework import serializers

from apps.core.serializers import DynamicFieldsModelSerializer
from apps.subscriptions.models import RevenueCatHistory, UserSubscription


class UserSubscriptionSerializer(DynamicFieldsModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserSubscription
        fields = (
            "user", "plan", "receipt",
            "subscription_type",
            "subscription_status", "expires_on",
        )
        read_only_fields = ("plan", "expires_on", "subscription_status")

    def create(self, validated_data):
        try:
            return UserSubscription.objects.get(receipt=validated_data.get("receipt"))
        
        except UserSubscription.MultipleObjectsReturned:
            return UserSubscription.objects.filter(
                receipt=validated_data.get("receipt")
            ).latest("created")
        
        except UserSubscription.DoesNotExist:
            return super().create(validated_data)


class RevenueCatHistorySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = RevenueCatHistory
        fields = (
            "event_id",
            "event_type",
            "app_user_id",
            "original_app_user_id",
            "product_id",
            "period_type",
            "purchased_at_ms",
            "expiration_at_ms",
            "event_timestamp_ms",
            "store",
            "environment",
            "cancel_reason",
            "is_trial_conversion",
        )


class MySubscriptionSerializer(serializers.Serializer):

    plan_name = serializers.CharField(source="plan.name", default=None)
    status = serializers.CharField(source="get_subscription_status_display")
    receipt = serializers.JSONField()
    amount_paid = serializers.IntegerField()
    subscribed_on = serializers.DateTimeField(source="created")
    expires_on = serializers.DateTimeField()

    class Meta:
        model = UserSubscription
