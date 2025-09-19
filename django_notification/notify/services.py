import logging
from http import HTTPStatus
import requests

from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

class NotificationService:
    CHANNELS = ["email", "sms", "telegram"]

    @staticmethod
    def send(notification):
        start_index = (
            NotificationService.CHANNELS.index(notification.channel)
            if notification.channel in NotificationService.CHANNELS
            else 0
        )
        channels_to_try = NotificationService.CHANNELS[start_index:]

        for channel in channels_to_try:
            try:
                if channel == "email":
                    NotificationService.send_email(notification)
                elif channel == "sms":
                    NotificationService.send_sms(notification)
                elif channel == "telegram":
                    NotificationService.send_telegram(notification)
                return
            except Exception as e:
                logger.exception(f"Ошибка при отправке через {channel}: {e}")
                continue

    @staticmethod
    def send_email(notification):
        try:
            send_mail(
                subject="Уведомление",
                message=notification.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.user.email],
                fail_silently=False,
            )
            notification.is_sent = True
            notification.save()
        except Exception as ex:
            raise ex

    @staticmethod
    def send_sms(notification):
        try:
            url = "https://sms.ru/sms/send"
            params = {
                "api_id": settings.API_ID,
                "to": notification.user.profile.phone_number,
                "msg": notification.message,
                "json": 1,
            }
            response = requests.get(url, params=params)
            if response.status_code != HTTPStatus.OK:
                raise Exception(f"Ошибка SMS: {response.text}")
            notification.is_sent = True
            notification.save()
        except Exception as ex:
            raise ex

    @staticmethod
    def send_telegram(notification):
        try:
            token = settings.TELEGRAM_BOT_TOKEN
            chat_id = notification.user.profile.telegram_chat_id
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            response = requests.post(
                url, data={"chat_id": chat_id, "text": notification.message}
            )
            if response.status_code != HTTPStatus.OK:
                raise Exception(f"Ошибка Telegram: {response.text}")
            notification.is_sent = True
            notification.save()
        except Exception as ex:
            raise ex
