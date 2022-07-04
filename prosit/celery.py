import os

# from django.conf import settings

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prosit.settings')


app = Celery('prosit')

# app.conf.update(timezone=settings.TIME_ZONE)

# app.conf.broker_url = 'redis://localhsost:6379/0'

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
	print(f"Request: {self.request!r}")