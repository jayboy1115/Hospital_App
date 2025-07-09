from rest_framework import serializers
from .models import Appointment
from django.utils import timezone

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor', 'appointment_time', 'status',
            'created_at', 'notes', 'reason', 'duration'
        ]
        read_only_fields = ['id', 'patient', 'status', 'created_at']

    def validate_appointment_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Appointment time must be in the future.")
        return value

    def validate(self, data):
        doctor = data.get('doctor')
        time   = data.get('appointment_time')
        if Appointment.objects.filter(doctor=doctor, appointment_time=time).exists():
            raise serializers.ValidationError("This slot is already booked.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        patient = user.patient
        return Appointment.objects.create(patient=patient, **validated_data)
