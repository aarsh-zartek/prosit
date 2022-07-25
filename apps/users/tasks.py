from django.db.models import BooleanField, Case, F, Q, When
from django.utils import timezone

from prosit.celery import app

from apps.notification.tasks import send_push_notification
from apps.subscriptions.models import UserSubscription
from apps.users.models import DailyActivity, User

from lib.constants import SubscriptionStatus


@app.task
def send_daily_weight_notification() -> str:
    subscribed_users = UserSubscription.objects.select_related("user").filter(
                plan__isnull=False,
                subscription_status=SubscriptionStatus.ACTIVE
            ).values('user')

    users = User.objects.prefetch_related("subscriptions").annotate(
        plan=Case(
            When(
                subscriptions__plan__isnull=False,
                then=F('subscriptions__plan'),
            ), default=False
        )
    )
    active_users = User.objects.prefetch_related('subscriptions').filter(
            subscriptions__isnull=False,
            subscriptions__plan__isnull=False,
            subscriptions__subscription_status=SubscriptionStatus.ACTIVE
        )

    no_of_users = 0
    activity_users = DailyActivity.objects.filter(users__in=users)# created__date=timezone.now().date()

    not_uploaded_users = activity_users.exclude(created__date=timezone.now().date())

    send_push_notification(
        users,
        title="Daily Weight Reminder",
        message="Enter your weight to track for your diet plan"
    )
    # Get List of subscribed users with a field `plan` assigned to him
    # Filter these users from daily activity
    # Exclude those who have uploaded data for `today`
    # Send notification to users

    return f"Notification sent to {no_of_users} users"

# Daily Activiy --> User <-- UserSubscription

# User.objects.prefetch_related("subscriptions", "daily_activity").filter(
#     subscription_status=SubscriptionStatus.ACTIVE
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

