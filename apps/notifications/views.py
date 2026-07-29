from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer



from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


# Notification ViewSet

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )  # User notifications

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )  # Save user

    @action(detail=True, methods=["patch"])  # Mark read
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return Response(
            NotificationSerializer(notification).data
        )

    @action(detail=False, methods=["patch"])  # Mark all
    def mark_all_read(self, request):
        self.get_queryset().update(
            is_read=True
        )

        return Response({
            "message": "All notifications marked as read."
        })

    @action(detail=False, methods=["get"])  # Unread count
    def unread(self, request):
        count = self.get_queryset().filter(
            is_read=False
        ).count()

        return Response({
            "unread_notifications": count
        })

    @action(detail=False, methods=["delete"])  # Delete all
    def clear(self, request):
        self.get_queryset().delete()

        return Response({
            "message": "Notifications cleared."
        })



# Notification Summary

    @action(detail=False, methods=["get"])
    def summary(self, request):

        qs = self.get_queryset()

        return Response({
            "total": qs.count(),
            "read": qs.filter(is_read=True).count(),
            "unread": qs.filter(is_read=False).count()
        })


# Recent Notification

    @action(detail=False, methods=["get"])
    def recent(self, request):

        qs = self.get_queryset()[:10]

        return Response(
            NotificationSerializer(qs, many=True).data
        )