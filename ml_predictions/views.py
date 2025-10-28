from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from patients.models import Patient
from .models import MLPrediction
from .ml_service import MLService
from .serializers import MLPredictionSerializer
import json
import os
from pathlib import Path

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_model_metrics(request):
    """Get ML model performance metrics"""
    try:
        # Load model summary from saved file
        base_dir = Path(__file__).resolve().parent.parent
        model_summary_path = base_dir / 'ML' / 'models_and_scalers' / 'model_summary.json'
        
        if model_summary_path.exists():
            with open(model_summary_path, 'r') as f:
                model_data = json.load(f)
            
            return Response({
                'success': True,
                'data': {
                    'model_name': model_data.get('best_model'),
                    'feature_selection': model_data.get('best_feature_set'),
                    'n_features': model_data.get('n_features'),
                    'selected_features': model_data.get('selected_features'),
                    'performance': {
                        'accuracy': round(model_data['performance']['accuracy'] * 100, 2),
                        'precision': round(model_data['performance']['precision'] * 100, 2),
                        'recall': round(model_data['performance']['recall'] * 100, 2),
                        'f1_score': round(model_data['performance']['f1_score'] * 100, 2),
                        'auc': round(model_data['performance']['auc'] * 100, 2)
                    },
                    'pca_analysis': model_data.get('pca_analysis'),
                    'model_version': '2.0.0-PCA'
                }
            })
        else:
            # Fallback metrics if file not found
            return Response({
                'success': True,
                'data': {
                    'model_name': 'Gradient Boosting',
                    'feature_selection': 'PCA-optimized',
                    'n_features': 15,
                    'performance': {
                        'accuracy': 92.47,
                        'precision': 94.03,
                        'recall': 98.03,
                        'f1_score': 95.99,
                        'auc': 81.81
                    },
                    'model_version': '2.0.0-PCA'
                }
            })
            
    except Exception as e:
        return Response({
            'success': False,
            'error': {'message': f'Failed to load model metrics: {str(e)}'}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_patient(request, patient_id):
    """Trigger ML analysis for a patient"""
    try:
        patient = get_object_or_404(Patient, id=patient_id)
        ml_service = MLService()
        
        prediction_result = ml_service.predict_ckd_risk(patient)
        
        # Save prediction to database
        prediction = MLPrediction.objects.create(
            patient=patient,
            prediction_result=prediction_result['result'],
            confidence=prediction_result['confidence'],
            predicted_stage=prediction_result['stage'],
            risk_level=prediction_result['risk_level'],
            input_data=prediction_result['input_metrics'],
            recommendations=prediction_result['recommendations'],
            model_version=prediction_result['model_version']
        )
        
        serializer = MLPredictionSerializer(prediction)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': {'message': str(e)}
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_prediction(request, patient_id):
    """Get latest ML prediction for a patient"""
    try:
        patient = get_object_or_404(Patient, id=patient_id)
        prediction = MLPrediction.objects.filter(patient=patient).first()
        
        if prediction:
            serializer = MLPredictionSerializer(prediction)
            return Response({
                'success': True,
                'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'error': {'message': 'No prediction found for this patient'}
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': {'message': str(e)}
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_prediction_history(request, patient_id):
    """Get prediction history for a patient"""
    try:
        patient = get_object_or_404(Patient, id=patient_id)
        predictions = MLPrediction.objects.filter(patient=patient).order_by('-created_at')
        
        serializer = MLPredictionSerializer(predictions, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'meta': {
                'count': predictions.count(),
                'patient_id': str(patient_id)
            }
        })
            
    except Exception as e:
        return Response({
            'success': False,
            'error': {'message': str(e)}
        }, status=status.HTTP_400_BAD_REQUEST)