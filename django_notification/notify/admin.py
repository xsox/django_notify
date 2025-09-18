from django.contrib import admin
from .models import Notification
from .tasks import send_notification_task


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "channel", "is_sent", "created_at")
    list_filter = ("channel", "is_sent", "created_at")
    search_fields = ("user__username", "user__email", "message")
    readonly_fields = ("created_at",)
    actions = ["mark_as_sent", "send_notification"]

    def mark_as_sent(self, request, queryset):
        updated = queryset.update(is_sent=True)
        self.message_user(request, f"{updated} уведомление(й) помечено(ы) как отправленные")
    mark_as_sent.short_description = "Пометить выбранные уведомления как отправленные"
    
    
    def send_notification(self, request, queryset):
        notify = queryset.objects.first()
        send_notification_task.apply_async(
            args=[notify.pk],
        )
    send_notification.short_description = "Отправить"