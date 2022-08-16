from django.db.models import BooleanField, Case, Q, When
from django.utils import timezone

from prosit.celery import app

from apps.notification.tasks import send_push_notification
from apps.users.models import User

from lib.constants import SubscriptionStatus


@app.task(name="Daily Weight Reminder Notification")
def send_daily_weight_notification() -> str:
    """Sends a reminder notification to enter daily weight"""
    
    users = User.objects.prefetch_related("subscriptions", "daily_activity").filter(
            subscriptions__subscription_status=SubscriptionStatus.ACTIVE
        ).annotate(
            subscribed=Case(
                When(
                    Q(subscriptions__isnull=False),
                    then=True
                ),
                default=False, output_field=BooleanField()
            ),
            plan_assigned=Case(
                When(
                    subscriptions__plan__isnull=False,
                    then=True
                ),
                default=False, output_field=BooleanField()
            ),
            weight_uploaded_today=Case(
                When(
                    daily_activity__created__date=timezone.now().date(),
                    then=True
                ),
                default=False, output_field=BooleanField()
            )
        ).filter(
            subscribed=True,
            plan_assigned=True,
            weight_uploaded_today=False
        )

    send_push_notification(
        users,
        title="Daily Weight Reminder",
        message="Enter your weight to track for your diet plan"
    )
    # Get List of subscribed users with a field `plan` assigned to him
    # Filter these users from daily activity
    # Exclude those who have uploaded data for `today`
    # Send notification to users

    return f"Daily reminder notification sent to {users.count()} users"

# Daily Activiy --> User <-- UserSubscription

# User.objects.prefetch_related("subscriptions", "daily_activity").filter(
#     subscriptions__subscription_status=SubscriptionStatus.ACTIVE
# ).annotate(
#     subscribed=Case(
#         When(
#             # Q(subscriptions__isnull=False) & Q(subscription_status=SubscriptionStatus.ACTIVE),
#             Q(subscriptions__isnull=False),
#             then=True
#         ),
#         default=False, output_field=BooleanField()
#     ),
#     plan_assigned=Case(
#         When(
#             subscriptions__plan__isnull=False,
#             then=True
#         ),
#         default=False, output_field=BooleanField()
#     ),
#     weight_uploaded_today=Case(
#         When(
#             daily_activity__created__date=timezone.now().date(),
#             then=True
#         ),
#         default=False, output_field=BooleanField()
#     )
# ).filter(
#     subscribed=True,
#     plan_assigned=True,
#     weight_uploaded_today=False
# )


# User.objects.prefetch_related(
#     "subscriptions", "daily_activity"
# ).filter(
#     subscriptions__isnull=False,
#     subscriptions__plan__isnull=False,
#     subscriptions__subscription_status=SubscriptionStatus.ACTIVE,
# ).exclude(
#     daily_activity__created__date=timezone.now().date()
# )

