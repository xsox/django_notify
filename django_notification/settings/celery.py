import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_notification.settings.local")

app = Celery("django_notification")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
