from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser

from django_notification.notify.models import Notification
from django_notification.notify.serializers import SendNotificationSerializer


class SendNotificationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,):
    permission_classes = [IsAdminUser]
    queryset = Notification.objects.all()
    serializer_class = SendNotificationSerializer