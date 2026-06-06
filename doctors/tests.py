"""
Tests for doctors module.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Doctor


class DoctorTests(APITestCase):
    """
    Tests for doctor endpoints.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='password123'
        )
        
        # Generate JWT token
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_create_doctor(self):
        """Test creating a new doctor."""
        data = {
            'name': 'Dr. kahan hirani',
            'specialization': 'Cardiology',
            'phone': '1234567890',
            'email': 'dr.kahan@example.com'
        }
        response = self.client.post('/api/doctors/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Dr. kahan hirani')
    
    def test_list_doctors(self):
        """Test listing all doctors."""
        Doctor.objects.create(
            name='Dr. One', specialization='Cardiology',
            phone='123', email='one@example.com'
        )
        Doctor.objects.create(
            name='Dr. Two', specialization='Neurology',
            phone='456', email='two@example.com'
        )
        
        response = self.client.get('/api/doctors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_update_doctor(self):
        """Test updating a doctor."""
        doctor = Doctor.objects.create(
            name='Dr. Old', specialization='Cardiology',
            phone='123', email='old@example.com'
        )
        
        data = {
            'name': 'Dr. New',
            'specialization': 'Neurology',
            'phone': '456',
            'email': 'new@example.com'
        }
        response = self.client.put(f'/api/doctors/{doctor.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Dr. New')
    
    def test_delete_doctor(self):
        """Test deleting a doctor."""
        doctor = Doctor.objects.create(
            name='Dr. Delete', specialization='Cardiology',
            phone='123', email='delete@example.com'
        )
        
        response = self.client.delete(f'/api/doctors/{doctor.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Doctor deleted successfully')
        self.assertFalse(Doctor.objects.filter(id=doctor.id).exists())
