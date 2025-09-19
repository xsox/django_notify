from rest_framework.routers import DefaultRouter

from django_notification.notify import views

app_name = "notify"
router = DefaultRouter()

router.register("send-notify", views.SendNotificationViewSet, basename="send_notify")

urlpatterns = router.urls
