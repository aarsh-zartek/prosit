from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework import status

from fcm_django.models import FCMDevice
from firebase_admin.messaging import (
    Message,
    Notification as FCMNotification,
)
from smtplib import SMTPAuthenticationError, SMTPConnectError

from prosit.celery import app
from prosit.settings import EMAIL_HOST_USER, PROSIT_ADMIN_EMAIL, DOMAIN_IP

from apps.notification.models import UserNotification

import logging

logger = logging.getLogger(__name__)

@app.task(name="Send Push notification")
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


@app.task(name="Send Email Notification")
def send_email_notificaton(data, *args, **kwargs) -> str:
    
    mail_msg = (
        f"<h3>Name: </h3>{data['name']}<br/>"
        f"<h3>Contact Number: </h3>{data['phone_number']}<br/>"
        f"<h3>Health Code: </h3>{data['health_code']}<br/>"
    )
    html_msg = render_to_string(
                'email.html',
                {
                    "message": mail_msg,
                    "url": f"{DOMAIN_IP}/admin/users/{data['id']}"
                }
            )
    msg = strip_tags(html_msg)

    response = {
        "message": "Error while sending message. Please contact Admin"
    }
    code = status.HTTP_401_UNAUTHORIZED
    try:
        send_mail(
            subject="New User awaiting Diet Plan assignment",
            message=msg,
            html_message=html_msg,
            recipient_list=PROSIT_ADMIN_EMAIL,
            from_email=EMAIL_HOST_USER,
            fail_silently=False
        )

    except SMTPAuthenticationError as smtpautherr:
        logger.exception(smtpautherr)
    except SMTPConnectError as smtpconnerr:
        logger.exception(smtpconnerr)
    except Exception as e:
        logger.exception(e)
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        response["message"] = "Email Sent Successfully"
        code = status.HTTP_200_OK
    
    return response, code
