"""
Views for mappings module.
"""

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer
from patients.models import Patient
from doctors.models import Doctor


class MappingListCreateView(generics.ListCreateAPIView):
    """
    GET /api/mappings/ - List all mappings
    POST /api/mappings/ - Create a new mapping
    """
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        """
        Add request to serializer context for validation.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        """
        Create mapping only if the patient belongs to the current user.
        """
        patient_id = serializer.validated_data.get('patient_id')
        
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            raise NotFound(detail={"error": "Patient not found"})
        
        # Check if patient belongs to current user
        if patient.created_by != self.request.user:
            raise PermissionDenied(detail="You can only map doctors to your own patients")
        
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        """
        Override create to handle validation errors properly.
        """
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            # Extract first error message for consistent format
            errors = serializer.errors
            first_key = list(errors.keys())[0]
            first_error = errors[first_key]
            if isinstance(first_error, list):
                error_message = first_error[0]
            else:
                error_message = str(first_error)
            
            return Response(
                {"error": error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PatientDoctorListView(generics.ListAPIView):
    """
    GET /api/mappings/{patient_id}/ - List all doctors mapped to a specific patient
    """
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return mappings for a specific patient that belongs to the current user.
        """
        patient_id = self.kwargs.get('patient_id')
        
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            raise NotFound(detail={"error": "Patient not found"})
        
        # Check if patient belongs to current user
        if patient.created_by != self.request.user:
            raise PermissionDenied(detail="You can only view mappings for your own patients")
        
        return PatientDoctorMapping.objects.filter(patient=patient)


class MappingDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/mappings/{id}/ - Delete a mapping
    """
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """
        Get the mapping object or raise 404 if not found.
        """
        pk = self.kwargs.get('pk')
        
        try:
            obj = PatientDoctorMapping.objects.get(pk=pk)
        except PatientDoctorMapping.DoesNotExist:
            raise NotFound(detail={"error": "Mapping not found"})
        
        return obj
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to return success response.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Mapping deleted successfully"}, status=status.HTTP_200_OK)
