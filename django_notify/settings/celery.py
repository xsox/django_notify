import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_notify.settings.local")

app = Celery("django_notify")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
