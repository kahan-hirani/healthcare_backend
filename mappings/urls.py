"""
URL configuration for mappings module.
"""

from django.urls import path
from .views import MappingListCreateView, PatientDoctorListView, MappingDeleteView

urlpatterns = [
    path('', MappingListCreateView.as_view(), name='mapping-list-create'),
    path('<int:patient_id>/', PatientDoctorListView.as_view(), name='patient-doctors'),
    path('delete/<int:pk>/', MappingDeleteView.as_view(), name='mapping-delete'),
]
