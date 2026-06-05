"""
Serializers for mappings module.
"""

from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for PatientDoctorMapping model.
    Handles creation of patient-doctor assignments.
    """
    patient_id = serializers.IntegerField(write_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient_id', 'doctor_id', 'patient_name', 'doctor_name', 'assigned_at']
        read_only_fields = ['id', 'assigned_at']
    
    def validate(self, data):
        """
        Validate that the patient and doctor exist and that mapping is unique.
        """
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        
        # Validate patient exists
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            raise serializers.ValidationError({"patient_id": "Patient not found"})
        
        # Validate doctor exists
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
        except Doctor.DoesNotExist:
            raise serializers.ValidationError({"doctor_id": "Doctor not found"})
        
        # Check for duplicate mapping
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError("This patient-doctor mapping already exists")
        
        return data
