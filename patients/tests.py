"""
Tests for patients module.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Patient


class PatientTests(APITestCase):
    """
    Tests for patient endpoints.
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
    
    def test_create_patient(self):
        """Test creating a new patient."""
        data = {
            'name': 'kahan hirani',
            'age': 30,
            'gender': 'Male',
            'phone': '1234567890',
            'address': '123 Main St'
        }
        response = self.client.post('/api/patients/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'kahan hirani')
        self.assertEqual(response.data['created_by'], self.user.id)
    
    def test_list_patients(self):
        """Test listing patients for authenticated user."""
        Patient.objects.create(
            name='Patient 1', age=25, gender='Male',
            phone='123', address='Addr 1', created_by=self.user
        )
        Patient.objects.create(
            name='Patient 2', age=30, gender='Female',
            phone='456', address='Addr 2', created_by=self.other_user
        )
        
        response = self.client.get('/api/patients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Patient 1')
    
    def test_update_patient(self):
        """Test updating own patient."""
        patient = Patient.objects.create(
            name='Old Name', age=25, gender='Male',
            phone='123', address='Addr', created_by=self.user
        )
        
        data = {'name': 'New Name', 'age': 26, 'gender': 'Male',
                'phone': '123', 'address': 'Addr'}
        response = self.client.put(f'/api/patients/{patient.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New Name')
    
    def test_delete_patient(self):
        """Test deleting own patient."""
        patient = Patient.objects.create(
            name='To Delete', age=25, gender='Male',
            phone='123', address='Addr', created_by=self.user
        )
        
        response = self.client.delete(f'/api/patients/{patient.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Patient deleted successfully')
        self.assertFalse(Patient.objects.filter(id=patient.id).exists())
