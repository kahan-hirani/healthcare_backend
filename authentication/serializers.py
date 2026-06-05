"""
Serializers for authentication module.
"""

from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    Validates name, email, and password fields.
    """
    name = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=6, write_only=True)
    
    def validate_email(self, value):
        """
        Validate that the email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def create(self, validated_data):
        """
        Create a new user using Django's create_user method.
        """
        name = validated_data['name']
        email = validated_data['email']
        password = validated_data['password']
        
        # Split name into first_name and last_name
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Validates email and password fields.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
