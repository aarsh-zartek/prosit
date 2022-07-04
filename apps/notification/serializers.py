from rest_framework import serializers

from apps.core.serializers import DynamicFieldsModelSerializer
from apps.notification.models import Notification


class NotificationSerializer(DynamicFieldsModelSerializer):

	class Meta:
		model = Notification
		fields = (
			"user", "title", "message",
			"read_at", "created"
		)

