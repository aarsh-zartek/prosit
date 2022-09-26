from django.utils import timezone

from prosit.celery import app

from apps.subscriptions.models import UserSubscription

from lib.constants import SubscriptionStatus


@app.task(name="Auto Expire User Subscription")
def convert_expired_subscriptions() -> str:
    """
    Changes user subscription status to `expired`
    """

    updated = UserSubscription.objects.filter(
                subscription_status=SubscriptionStatus.ACTIVE,
                expires_on__lte=timezone.now()
            ).update(subscription_status=SubscriptionStatus.EXPIRED)

    return f"{updated} user subscriptions updated"
