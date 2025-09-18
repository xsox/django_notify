from django.core.mail import send_mail
from django.conf import settings
import requests

class NotificationService:
    @staticmethod
    def send(notification):
        if notification.channel == "email":
            NotificationService.send_email(notification)
        elif notification.channel == "sms":
            NotificationService.send_sms(notification)
        elif notification.channel == "telegram":
            NotificationService.send_telegram(notification)

    @staticmethod
    def send_email(notification):
        send_mail(
            subject="Уведомление",
            message=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.user.email],
            fail_silently=False,
        )
        notification.is_sent = True
        notification.save()

    @staticmethod
    def send_sms(notification):
        print(f"[SMS] Отправка на {notification.user.profile.phone_number}: {notification.message}")
        notification.is_sent = True
        notification.save()

    @staticmethod
    def send_telegram(notification):
        token = settings.TELEGRAM_BOT_TOKEN
        chat_id = notification.user.profile.telegram_chat_id
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        response = requests.post(url, data={
            "chat_id": chat_id,
            "text": notification.message
        })
        if response.status_code == 200:
            notification.is_sent = True
            notification.save()
