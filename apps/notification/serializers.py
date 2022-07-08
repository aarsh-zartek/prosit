from rest_framework import serializers

from apps.core.serializers import DynamicFieldsModelSerializer
from apps.notification.models import UserNotification


class UserNotificationSerializer(DynamicFieldsModelSerializer):

	class Meta:
		model = UserNotification
		fields = (
			"id", "user", "title", "message",
			"read_at", "created"
		)
	