
from django.http import JsonResponse

from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from apps.notification.models import Notification
from apps.notification.serializers import NotificationSerializer
from apps.notification.tasks import run_task

# Create your views here.


class NotificationViewSet(
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	GenericViewSet
):

	serializer_class = NotificationSerializer
	queryset = Notification.objects.all()

	permission_classes = (IsAuthenticated,)


def test_celery(request):
	run_task.delay()

	return JsonResponse(data={'message': "Done"}, status=HTTP_200_OK)