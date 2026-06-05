"""
Models for doctors module.
"""

from django.db import models


class Doctor(models.Model):
    """
    Doctor model representing a doctor in the system.
    """
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.specialization}"
