from typing import Any
from django.utils import timezone
from lib.constants import SubscriptionStatus


class ExpireSubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request) -> Any:

        from apps.users.models import User
        from apps.subscriptions.models import UserSubscription

        response = self.get_response(request)
        user: User = request.user

        if user.is_authenticated:
            subscription: UserSubscription = user.active_subscription
            if subscription and subscription.expires_on <= timezone.now():
                subscription.subscription_status = SubscriptionStatus.EXPIRED
                subscription.save()

        return response
