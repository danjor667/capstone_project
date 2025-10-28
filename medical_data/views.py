from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from patients.models import Patient
from .models import KidneyMetrics, LabResult, Medication, VitalSigns
from .serializers import (
    KidneyMetricsSerializer, LabResultSerializer, 
    MedicationSerializer, VitalSignsSerializer
)

class MedicalDataViewSet(viewsets.ViewSet):
    
    @action(detail=True, methods=['get', 'post'], url_path='metrics')
    def kidney_metrics(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk)
        
        if request.method == 'GET':
            metrics = KidneyMetrics.objects.filter(patient=patient).order_by('-timestamp')[:1]
            serializer = KidneyMetricsSerializer(metrics, many=True)
            return Response({
                'success': True,
                'data': serializer.data[0] if serializer.data else None
            })
        
        elif request.method == 'POST':
            serializer = KidneyMetricsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(patient=patient)
                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'success': False,
                'error': {'message': 'Invalid data', 'details': serializer.errors}
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path='metrics/history')
    def metrics_history(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk)
        metrics = KidneyMetrics.objects.filter(patient=patient).order_by('-timestamp')
        serializer = KidneyMetricsSerializer(metrics, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=True, methods=['get', 'post'], url_path='lab-results')
    def lab_results(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk)
        
        if request.method == 'GET':
            results = LabResult.objects.filter(patient=patient).order_by('-test_date')
            serializer = LabResultSerializer(results, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        
        elif request.method == 'POST':
            serializer = LabResultSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(patient=patient)
                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'success': False,
                'error': {'message': 'Invalid data', 'details': serializer.errors}
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get', 'post'], url_path='medications')
    def medications(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk)
        
        if request.method == 'GET':
            medications = Medication.objects.filter(patient=patient, is_active=True)
            serializer = MedicationSerializer(medications, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        
        elif request.method == 'POST':
            serializer = MedicationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(patient=patient)
                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'success': False,
                'error': {'message': 'Invalid data', 'details': serializer.errors}
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get', 'post'], url_path='vitals')
    def vital_signs(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk)
        
        if request.method == 'GET':
            vitals = VitalSigns.objects.filter(patient=patient).order_by('-timestamp')
            serializer = VitalSignsSerializer(vitals, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        
        elif request.method == 'POST':
            serializer = VitalSignsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(patient=patient)
                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'success': False,
                'error': {'message': 'Invalid data', 'details': serializer.errors}
            }, status=status.HTTP_400_BAD_REQUEST)

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data
        })