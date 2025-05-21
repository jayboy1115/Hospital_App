from django.urls import path
from .views import (
    PatientAppointmentListCreateView,
    AppointmentDetailView,
    DoctorAppointmentListView,
)

urlpatterns = [
    path('my/', PatientAppointmentListCreateView.as_view(), name='patient-appointments'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('doctor/', DoctorAppointmentListView.as_view(), name='doctor-appointments'),
]
