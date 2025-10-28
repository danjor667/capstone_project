from rest_framework import serializers
from .models import Alert, Notification

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = [
            'id', 'type', 'title', 'message', 'priority', 'category',
            'acknowledged', 'acknowledged_by', 'acknowledged_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'type', 'title', 'message', 'read', 'data', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']