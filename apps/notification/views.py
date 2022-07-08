
from django.http import JsonResponse

from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from firebase_admin.messaging import Message, Notification

from apps.notification.models import UserNotification
from apps.notification.serializers import UserNotificationSerializer
from apps.notification.tasks import run_task

# Create your views here.


class UserNotificationViewSet(
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	GenericViewSet
):

	serializer_class = UserNotificationSerializer
	queryset = UserNotification.objects.all()

	permission_classes = (IsAuthenticated,)


def test_celery(request):
	run_task.delay()

	return JsonResponse(data={'message': "Done"}, status=HTTP_200_OK)