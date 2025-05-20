from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatbotSession
from .serializers import ChatbotSessionSerializer

RULES = {
    'headache': ('Paracetamol 500mg', 'Stay hydrated and rest.'),
    'fever': ('Ibuprofen 200mg', 'Monitor temperature; see doctor if > 39°C.'),
    'cough': ('Dextromethorphan syrup', 'Keep warm, drink warm fluids.'),
    # add more as needed...
}

class ChatbotAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            patient = user.patient
        except AttributeError:
            return Response({'detail':'Only patients can use chatbot.'}, status=status.HTTP_403_FORBIDDEN)

        symptoms = request.data.get('symptoms', '').lower()
        if not symptoms:
            return Response({'symptoms':['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

        for keyword, (drug, advice) in RULES.items():
            if keyword in symptoms:
                suggested_drugs = drug
                recommendation  = advice
                break
        else:
            suggested_drugs = 'Paracetamol 500mg'
            recommendation  = 'Please see a doctor for a proper diagnosis.'

        session = ChatbotSession.objects.create(
            patient=patient,
            symptoms=symptoms,
            suggested_drugs=suggested_drugs,
            recommendation=recommendation
        )

        serializer = ChatbotSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
