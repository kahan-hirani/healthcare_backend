"""
Tests for mappings module.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from patients.models import Patient
from doctors.models import Doctor
from .models import PatientDoctorMapping


class MappingTests(APITestCase):
    """
    Tests for mapping endpoints.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='password123'
        )
        self.other_user = User.objects.create_user(
            username='other@example.com',
            email='other@example.com',
            password='password123'
        )
        
        # Generate JWT token
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Create test data
        self.patient = Patient.objects.create(
            name='Test Patient', age=30, gender='Male',
            phone='123', address='Addr', created_by=self.user
        )
        self.other_patient = Patient.objects.create(
            name='Other Patient', age=25, gender='Female',
            phone='456', address='Other Addr', created_by=self.other_user
        )
        self.doctor = Doctor.objects.create(
            name='Dr. Test', specialization='Cardiology',
            phone='789', email='dr@test.com'
        )
    
    def test_create_mapping_success(self):
        """Test creating a mapping for own patient."""
        data = {
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id
        }
        response = self.client.post('/api/mappings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['patient_name'], 'Test Patient')
        self.assertEqual(response.data['doctor_name'], 'Dr. Test')
    
    def test_create_mapping_for_other_patient(self):
        """Test creating a mapping for another user's patient."""
        data = {
            'patient_id': self.other_patient.id,
            'doctor_id': self.doctor.id
        }
        response = self.client.post('/api/mappings/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_duplicate_mapping(self):
        """Test creating a duplicate mapping."""
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        
        data = {
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id
        }
        response = self.client.post('/api/mappings/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_mappings(self):
        """Test listing all mappings."""
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        
        response = self.client.get('/api/mappings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_list_patient_doctors(self):
        """Test listing doctors for a specific patient."""
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        
        response = self.client.get(f'/api/mappings/{self.patient.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['doctor_name'], 'Dr. Test')
    
    def test_delete_mapping(self):
        """Test deleting a mapping."""
        mapping = PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        
        response = self.client.delete(f'/api/mappings/delete/{mapping.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PatientDoctorMapping.objects.filter(id=mapping.id).exists())
