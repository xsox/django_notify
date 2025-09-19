from celery import shared_task
from .models import Notification
from .services import NotificationService


@shared_task
def send_notification_task(notification_id):
    notif = Notification.objects.get(id=notification_id)
    NotificationService.send(notif)
