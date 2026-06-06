"""
Tests for authentication module.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class AuthenticationTests(APITestCase):
    """
    Tests for authentication endpoints.
    """
    
    def test_register_success(self):
        """Test successful user registration."""
        data = {
            'name': 'kahan',
            'email': 'kahan@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully')
        self.assertTrue(User.objects.filter(email='kahan@example.com').exists())
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email."""
        User.objects.create_user(username='kahan@example.com', email='kahan@example.com')
        data = {
            'name': 'kahan',
            'email': 'kahan@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_success(self):
        """Test successful login."""
        User.objects.create_user(username='kahan@example.com', email='kahan@example.com', password='password123')
        data = {
            'email': 'kahan@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
