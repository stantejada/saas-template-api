from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Subscription
from .serializers import SubscriptionSerializers


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan = request.data.get('plan')
        if plan not in ['free', 'pro', 'enterprise']:
            return Response({'datail':'Invalid plan'}, status = status.HTTP_400_BAD_REQUEST)
        
        # checkout simulation
        session_id = 'mock_session_' + plan
        return Response({'session_id': session_id, 'plan':plan})
    
class ConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session_id = request.data.get('session_id')
        if not session_id or not session_id.startswith('mock_session_'):
            return Response({'detail':'Invalid session'}, status=status.HTTP_400_BAD_REQUEST)
        
        plan = session_id.replace("mock_session_", "")

        #mocking update or create a subscription
        subscription, created = Subscription.objects.get_or_create(user=request.user)
        subscription.plan = plan
        subscription.active = True
        subscription.save()

        return Response({'detail':f"Subscription updated to {plan}"})



