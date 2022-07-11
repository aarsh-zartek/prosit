from django.http import JsonResponse
from django.utils import timezone

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from firebase_admin import get_app

from apps.notification.models import UserNotification
from apps.notification.serializers import UserNotificationSerializer

import logging

logger = logging.getLogger(__name__)

# Create your views here.


class UserNotificationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = UserNotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserNotification.objects.filter(
            user=self.request.user, read_at__isnull=True
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        self.get_queryset().update(read_at=timezone.now())
        return response

    @action(methods=["patch"], detail=False)
    def mark_read(self, request, *args, **kwargs):
        try:
            notifications = self.get_queryset().update(read_at=timezone.now())
        except Exception as e:
            logger.exception(e)
            return Response(
                {"message": "Could not update notifications"},
                status=HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "All Notifications marked as read."}, status=HTTP_200_OK
        )
