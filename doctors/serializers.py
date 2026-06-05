"""
Serializers for doctors module.
"""

from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model.
    Handles creation and update of doctor records.
    """
    
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'phone', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_email(self, value):
        """
        Validate email uniqueness.
        Check if a doctor with this email already exists (excluding current instance on update).
        """
        instance = getattr(self, 'instance', None)
        queryset = Doctor.objects.filter(email=value)
        
        if instance:
            queryset = queryset.exclude(pk=instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("Email already exists")
        
        return value
