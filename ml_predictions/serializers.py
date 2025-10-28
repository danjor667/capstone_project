from rest_framework import serializers
from .models import MLPrediction, RiskFactor, TrendAnalysis

class MLPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLPrediction
        fields = [
            'id', 'prediction_result', 'confidence', 'predicted_stage',
            'risk_level', 'input_data', 'recommendations', 'model_version',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class RiskFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskFactor
        fields = [
            'id', 'factor_name', 'factor_type', 'impact_score',
            'description', 'is_modifiable', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class TrendAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendAnalysis
        fields = [
            'id', 'trend_type', 'trend_data', 'slope', 'r_squared',
            'prediction_horizon_days', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']