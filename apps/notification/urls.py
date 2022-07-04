from cProfile import run
from django.urls import path, include

from apps.notification.views import test_celery


urlpatterns = [
	path("test_celery", test_celery, name="test_celery")
]
