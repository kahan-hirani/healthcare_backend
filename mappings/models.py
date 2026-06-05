"""
Models for mappings module.
"""

from django.db import models
from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMapping(models.Model):
    """
    PatientDoctorMapping model representing the assignment of a doctor to a patient.
    Ensures no duplicate assignments through unique constraint.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['patient', 'doctor'],
                name='unique_patient_doctor_mapping'
            )
        ]
    
    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name}"
