"""
Views for doctors module.
"""

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorListCreateView(generics.ListCreateAPIView):
    """
    GET /api/doctors/ - List all doctors
    POST /api/doctors/ - Create a new doctor
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/doctors/{id}/ - Retrieve a doctor
    PUT /api/doctors/{id}/ - Update a doctor
    DELETE /api/doctors/{id}/ - Delete a doctor
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """
        Get the doctor object or raise 404 if not found.
        """
        queryset = self.get_queryset()
        pk = self.kwargs.get('pk')
        
        try:
            obj = queryset.get(pk=pk)
        except Doctor.DoesNotExist:
            raise NotFound(detail={"error": "Doctor not found"})
        
        return obj
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to return success message.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Doctor deleted successfully"},
            status=status.HTTP_200_OK
        )
