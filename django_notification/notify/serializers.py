from rest_framework import serializers

from django_notification.notify.models import Notification
from django_notification.notify.tasks import send_notification_task


class SendNotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = ["user", "channel", "message"]
        
    def create(self, validated_data):
        notification = super().create(validated_data)
        send_notification_task.apply_async(
            args=[notification.pk],
        )
        if not notification.is_sent:
            raise serializers.ValidationError("Произошла ошибка отправки")
        return notification