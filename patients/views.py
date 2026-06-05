"""
Views for patients module.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from .models import Patient
from .serializers import PatientSerializer
from core.permissions import IsOwnerPermission


class PatientListCreateView(generics.ListCreateAPIView):
    """
    GET /api/patients/ - List all patients created by the current user
    POST /api/patients/ - Create a new patient
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only patients created by the current user.
        """
        return Patient.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        """
        Automatically set created_by to the current user.
        """
        serializer.save(created_by=self.request.user)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/patients/{id}/ - Retrieve a patient
    PUT /api/patients/{id}/ - Update a patient
    DELETE /api/patients/{id}/ - Delete a patient
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]
    
    def get_queryset(self):
        """
        Return only patients created by the current user.
        """
        return Patient.objects.filter(created_by=self.request.user)
    
    def get_object(self):
        """
        Get the patient object or raise 404 if not found or not owned by user.
        """
        queryset = self.get_queryset()
        pk = self.kwargs.get('pk')
        
        try:
            obj = queryset.get(pk=pk)
        except Patient.DoesNotExist:
            raise NotFound(detail={"error": "Patient not found"})
        
        self.check_object_permissions(self.request, obj)
        return obj
