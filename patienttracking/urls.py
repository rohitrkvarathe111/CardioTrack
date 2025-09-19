from django.urls import path
from .views import PatientDataAPIView, ViewPatientDataAPIView

urlpatterns = [

    path('patient_data', PatientDataAPIView.as_view(), name='patient_data'),
    path('view_patient_data', ViewPatientDataAPIView.as_view(), name='view_patient_data'),


]


