from rest_framework import generics, permissions
from .models import Patient
from .serializers import PatientProfileSerializer

class PatientProfileUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PatientProfileSerializer

    def get_object(self):
        return Patient.objects.get(user=self.request.user)
