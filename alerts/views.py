from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from patients.models import Patient
from .models import Alert, Notification
from .serializers import AlertSerializer, NotificationSerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    
    @action(detail=True, methods=['get'], url_path='alerts')
    def patient_alerts(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk)
        alerts = Alert.objects.filter(patient=patient).order_by('-created_at')
        serializer = AlertSerializer(alerts, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=True, methods=['put'], url_path='acknowledge')
    def acknowledge_alert(self, request, pk=None):
        alert = get_object_or_404(Alert, pk=pk)
        alert.acknowledged = True
        alert.acknowledged_by = request.user
        alert.acknowledged_at = timezone.now()
        alert.save()
        
        serializer = AlertSerializer(alert)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data
        }, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({
            'success': True,
            'message': 'Alert dismissed successfully'
        }, status=status.HTTP_204_NO_CONTENT)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data['results'] if 'results' in response.data else response.data
        })
    
    @action(detail=True, methods=['put'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.read = True
        notification.save()
        
        serializer = NotificationSerializer(notification)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=False, methods=['put'], url_path='mark-all-read')
    def mark_all_read(self, request):
        Notification.objects.filter(user=request.user, read=False).update(read=True)
        return Response({
            'success': True,
            'message': 'All notifications marked as read'
        })