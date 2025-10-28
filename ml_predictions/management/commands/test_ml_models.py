from django.core.management.base import BaseCommand
from patients.models import Patient
from ml_predictions.ml_service import MLService
from ml_predictions.models import MLPrediction

class Command(BaseCommand):
    help = 'Test the PCA-optimized ML models with existing patients'
    
    def add_arguments(self, parser):
        parser.add_argument('--patient-id', type=str, help='Test specific patient by ID')
        parser.add_argument('--count', type=int, default=5, help='Number of patients to test')
    
    def handle(self, *args, **options):
        self.stdout.write('Testing PCA-optimized ML models...')
        
        # Initialize ML service
        ml_service = MLService()
        
        if options['patient_id']:
            # Test specific patient
            try:
                patient = Patient.objects.get(id=options['patient_id'])
                self.test_patient_prediction(ml_service, patient)
            except Patient.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Patient {options["patient_id"]} not found'))
        else:
            # Test multiple patients
            patients = Patient.objects.filter(kidney_metrics__isnull=False).distinct()[:options['count']]
            
            if not patients:
                self.stdout.write(self.style.WARNING('No patients with kidney metrics found'))
                return
            
            self.stdout.write(f'Testing {len(patients)} patients...')
            
            for i, patient in enumerate(patients, 1):
                self.stdout.write(f'\n--- Patient {i}: {patient.first_name} {patient.last_name} ---')
                self.test_patient_prediction(ml_service, patient)
        
        self.stdout.write(self.style.SUCCESS('\nML model testing completed!'))
    
    def test_patient_prediction(self, ml_service, patient):
        """Test ML prediction for a single patient"""
        try:
            # Get patient's latest metrics for context
            latest_metrics = patient.kidney_metrics.order_by('-timestamp').first()
            if latest_metrics:
                self.stdout.write(f'Latest eGFR: {latest_metrics.egfr}, Creatinine: {latest_metrics.creatinine}')
            
            # Run ML prediction
            prediction_result = ml_service.predict_ckd_risk(patient)
            
            # Display results
            self.stdout.write(f'ML Prediction Results:')
            self.stdout.write(f'  Result: {prediction_result["result"]}')
            self.stdout.write(f'  Confidence: {prediction_result["confidence"]}%')
            self.stdout.write(f'  Risk Level: {prediction_result["risk_level"]}')
            self.stdout.write(f'  CKD Stage: {prediction_result["stage"]}')
            self.stdout.write(f'  Model Version: {prediction_result["model_version"]}')
            
            if prediction_result["recommendations"]:
                self.stdout.write(f'  Recommendations:')
                for rec in prediction_result["recommendations"]:
                    self.stdout.write(f'    - {rec}')
            
            # Save prediction to database
            MLPrediction.objects.create(
                patient=patient,
                prediction_result=prediction_result["result"],
                confidence=prediction_result["confidence"],
                predicted_stage=prediction_result["stage"],
                risk_level=prediction_result["risk_level"],
                input_data=prediction_result["input_metrics"],
                recommendations=prediction_result["recommendations"],
                model_version=prediction_result["model_version"]
            )
            
            self.stdout.write(self.style.SUCCESS('  ✓ Prediction saved to database'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ✗ Prediction failed: {str(e)}'))