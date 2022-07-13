from fcm_django.models import FCMDevice
from firebase_admin.messaging import (
    Message,
    Notification as FCMNotification,
)
from prosit.celery import app

from apps.notification.models import UserNotification


@app.task
def send_push_notification(users, **kwargs):
    """Send Push Notification to users"""

    devices = FCMDevice.objects.filter(user__in=users, active=True)
    devices.send_message(
        Message(
            notification=FCMNotification(
                title=kwargs.get("title", ""), body=kwargs.get("message", "")
            ),
            data=kwargs.get("data"),
        )
    )

    user_notifications = [
        UserNotification(
            user=user,
            title=kwargs.get("title", ""),
            message=kwargs.get("message", ""),
        )
        for user in users
    ]

    notifications = UserNotification.objects.bulk_create(user_notifications)

    return "Notifications Sent to all the users."


@app.task
def send_email_notificaton(*args, **kwargs) -> str:

    return "Email Sent Successfully"
