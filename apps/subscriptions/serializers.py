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
        read_only_fields = ("plan",)

    def create(self, validated_data):
        try:
            return UserSubscription.objects.get(receipt=validated_data.get("receipt"))
        
        except UserSubscription.MultipleObjectsReturned:
            return UserSubscription.objects.filter(
                receipt=validated_data.get("receipt")
            ).latest("created")
        
        except UserSubscription.DoesNotExist:
            return super().create(validated_data)


class VerifyPurchaseSerializer(serializers.Serializer):
    purchase_verified = serializers.SerializerMethodField()

    def get_purchase_verified(self, instance: UserSubscription) -> bool:
        return instance.user.uid

    class Meta:
        model = UserSubscription
        fields = ("purchase_verified",)


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
