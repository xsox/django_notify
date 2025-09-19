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

    def send_notification(self, request, queryset):
        for notification in queryset:
            send_notification_task.apply_async(
                args=[notification.pk],
            )

    send_notification.short_description = "Отправить"
