from django.urls import path
from .views import PatientProfileUpdateView

urlpatterns = [
    path('me/profile/', PatientProfileUpdateView.as_view(), name='patient-profile'),
]