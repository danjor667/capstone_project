import pandas as pd
import numpy as np
import joblib
import os
from django.conf import settings
from pathlib import Path

class MLService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.selected_features = None
        self.model_version = "2.0.0-PCA"
        self.load_model()
    
    def load_model(self):
        """Load the trained PCA-optimized ML model"""
        try:
            # Path to saved models
            base_dir = Path(__file__).resolve().parent.parent
            models_dir = base_dir / 'ML' / 'models_and_scalers'
            
            # Load trained model components
            model_path = models_dir / 'best_ckd_model.pkl'
            scaler_path = models_dir / 'feature_scaler.pkl'
            features_path = models_dir / 'selected_features.pkl'
            
            if all(path.exists() for path in [model_path, scaler_path, features_path]):
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                self.selected_features = joblib.load(features_path)
                print(f"Loaded PCA-optimized model with {len(self.selected_features)} features")
            else:
                print("Trained models not found, using fallback")
                self._create_fallback_model()
                
        except Exception as e:
            print(f"Error loading ML model: {e}")
            self._create_fallback_model()
    
    def _create_fallback_model(self):
        """Create fallback rule-based system if models not available"""
        self.model = None
        self.scaler = None
        self.selected_features = ['Age', 'GFR', 'SerumCreatinine', 'SystolicBP', 'ProteinInUrine']
        print("Using rule-based fallback system")
    
    def extract_patient_features(self, patient):
        """Extract features from patient data matching the trained model"""
        from medical_data.models import KidneyMetrics, VitalSigns, LabResult
        from datetime import date
        
        # Get latest data
        latest_metrics = KidneyMetrics.objects.filter(patient=patient).order_by('-timestamp').first()
        latest_vitals = VitalSigns.objects.filter(patient=patient).order_by('-timestamp').first()
        
        if not latest_metrics:
            raise ValueError("No kidney metrics found for patient")
        
        # Calculate age
        age = date.today().year - patient.date_of_birth.year
        
        # Feature mapping (map model features to available data)
        feature_map = {
            'Age': age,
            'GFR': float(latest_metrics.egfr),
            'SerumCreatinine': float(latest_metrics.creatinine),
            'SystolicBP': latest_vitals.systolic_bp if latest_vitals else latest_metrics.systolic_bp or 120,
            'DiastolicBP': latest_vitals.diastolic_bp if latest_vitals else latest_metrics.diastolic_bp or 80,
            'ProteinInUrine': float(latest_metrics.proteinuria) if latest_metrics.proteinuria else 0,
            'BMI': 25.0,  # Default if not available
            'HemoglobinLevels': 12.0,  # Default if not available
            'BUNLevels': 20.0,  # Default if not available
        }
        
        # Get lab results for additional features
        recent_labs = LabResult.objects.filter(patient=patient).order_by('-test_date')[:10]
        for lab in recent_labs:
            if lab.test_name == 'Hemoglobin' and 'HemoglobinLevels' in feature_map:
                feature_map['HemoglobinLevels'] = float(lab.value)
            elif lab.test_name == 'BUN' and 'BUNLevels' in feature_map:
                feature_map['BUNLevels'] = float(lab.value)
        
        # Extract only selected features in correct order
        if self.selected_features:
            features = []
            for feature_name in self.selected_features:
                if feature_name in feature_map:
                    features.append(feature_map[feature_name])
                else:
                    # Use reasonable defaults for missing features
                    features.append(0.0)
            return np.array(features).reshape(1, -1)
        else:
            # Fallback to basic features
            return np.array([
                age, float(latest_metrics.egfr), float(latest_metrics.creatinine),
                latest_vitals.systolic_bp if latest_vitals else 120,
                float(latest_metrics.proteinuria) if latest_metrics.proteinuria else 0
            ]).reshape(1, -1)
    
    def predict_ckd_risk(self, patient):
        """Predict CKD risk using trained PCA-optimized model"""
        try:
            # Extract features
            features = self.extract_patient_features(patient)
            
            if self.model is not None and self.scaler is not None:
                # Use trained model
                features_scaled = self.scaler.transform(features)
                prediction_proba = self.model.predict_proba(features_scaled)[0]
                prediction = self.model.predict(features_scaled)[0]
                confidence = np.max(prediction_proba) * 100
                
                # Convert binary prediction to meaningful result
                if prediction == 1:
                    result = "CKD Positive"
                    risk_level = self._get_risk_level_from_confidence(confidence)
                else:
                    result = "CKD Negative"
                    risk_level = "low"
                
            else:
                # Fallback to rule-based system
                latest_metrics = patient.kidney_metrics.order_by('-timestamp').first()
                egfr = float(latest_metrics.egfr)
                
                if egfr < 30:
                    prediction, result, risk_level, confidence = 1, "CKD Stage 4-5", "critical", 90.0
                elif egfr < 60:
                    prediction, result, risk_level, confidence = 1, "CKD Stage 3", "high", 85.0
                elif egfr < 90:
                    prediction, result, risk_level, confidence = 1, "CKD Stage 2", "medium", 75.0
                else:
                    prediction, result, risk_level, confidence = 0, "Normal Kidney Function", "low", 80.0
            
            # Generate recommendations
            recommendations = self._generate_recommendations(prediction, patient)
            
            # Get input metrics for display
            input_metrics = self._get_input_metrics_summary(patient)
            
            return {
                'result': result,
                'confidence': round(confidence, 2),
                'stage': self._get_stage_from_prediction(prediction, patient),
                'risk_level': risk_level,
                'input_metrics': input_metrics,
                'recommendations': recommendations,
                'model_version': self.model_version
            }
            
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
    
    def _get_risk_level_from_confidence(self, confidence):
        """Determine risk level based on model confidence"""
        if confidence >= 90:
            return 'critical'
        elif confidence >= 80:
            return 'high'
        elif confidence >= 70:
            return 'medium'
        else:
            return 'low'
    
    def _get_stage_from_prediction(self, prediction, patient):
        """Get CKD stage from prediction and patient data"""
        if prediction == 0:
            return 1  # Normal/Stage 1
        
        # Use eGFR to determine stage for positive predictions
        latest_metrics = patient.kidney_metrics.order_by('-timestamp').first()
        if latest_metrics:
            egfr = float(latest_metrics.egfr)
            if egfr >= 90:
                return 1
            elif egfr >= 60:
                return 2
            elif egfr >= 30:
                return 3
            elif egfr >= 15:
                return 4
            else:
                return 5
        return 3  # Default
    
    def _get_input_metrics_summary(self, patient):
        """Get summary of input metrics used for prediction"""
        from datetime import date
        
        latest_metrics = patient.kidney_metrics.order_by('-timestamp').first()
        latest_vitals = patient.vital_signs.order_by('-timestamp').first()
        
        age = date.today().year - patient.date_of_birth.year
        
        return {
            'age': age,
            'bloodPressure': f"{latest_vitals.systolic_bp if latest_vitals else latest_metrics.systolic_bp or 120}/{latest_vitals.diastolic_bp if latest_vitals else latest_metrics.diastolic_bp or 80}",
            'serumCreatinine': float(latest_metrics.creatinine) if latest_metrics else 0,
            'bloodUrea': 0,  # Would need lab results
            'hemoglobin': 0,  # Would need lab results
            'eGFR': float(latest_metrics.egfr) if latest_metrics else 0
        }
    
    def _get_risk_level(self, stage, egfr):
        """Determine risk level based on stage and eGFR"""
        if stage >= 4 or egfr < 30:
            return 'critical'
        elif stage == 3 or egfr < 60:
            return 'high'
        elif stage == 2 or egfr < 90:
            return 'medium'
        else:
            return 'low'
    
    def _generate_recommendations(self, prediction, patient):
        """Generate recommendations based on prediction and patient data"""
        recommendations = []
        
        latest_metrics = patient.kidney_metrics.order_by('-timestamp').first()
        if not latest_metrics:
            return ["Insufficient data for recommendations"]
        
        egfr = float(latest_metrics.egfr)
        
        # Stage-based recommendations
        if egfr < 15:
            recommendations.extend([
                "Immediate nephrology consultation required",
                "Prepare for renal replacement therapy",
                "Strict dietary and fluid restrictions"
            ])
        elif egfr < 30:
            recommendations.extend([
                "Urgent nephrology referral needed",
                "Consider dialysis preparation",
                "Monitor for complications"
            ])
        elif egfr < 60:
            recommendations.extend([
                "Regular nephrology follow-up",
                "Monitor blood pressure closely",
                "Protein restriction may be needed"
            ])
        elif egfr < 90:
            recommendations.extend([
                "Annual kidney function monitoring",
                "Blood pressure control",
                "Maintain healthy lifestyle"
            ])
        else:
            recommendations.extend([
                "Continue regular health checkups",
                "Maintain healthy diet and exercise",
                "Monitor blood pressure"
            ])
        
        # Specific recommendations based on metrics
        if latest_metrics.systolic_bp and latest_metrics.systolic_bp > 140:
            recommendations.append("Blood pressure management needed")
        
        if latest_metrics.proteinuria and latest_metrics.proteinuria > 1:
            recommendations.append("Consider protein intake reduction")
        
        if float(latest_metrics.creatinine) > 2.0:
            recommendations.append("Monitor kidney function closely")
        
        return recommendations