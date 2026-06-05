"""
Serializers for patients module.
"""

from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.
    Handles creation and update of patient records.
    """
    
    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'gender', 'phone', 'address', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']
    
    def validate_age(self, value):
        """
        Validate that age is greater than 0.
        """
        if value <= 0:
            raise serializers.ValidationError("Age must be greater than 0")
        return value
