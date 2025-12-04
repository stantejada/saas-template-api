from django.shortcuts import render

from rest_framework import viewsets, filters, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView



from . import models, serializers
from . import permissions
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer

from users.models import UserProfile

# Create your views here.

class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handle creating and updating user profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserRegistrationView(generics.CreateAPIView):
    """ Register a new user"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get('token')
        try:
            user = UserProfile.objects.get(verification_token=token)
            user.is_verified = True
            user.verification_token = None
            user.save()
            return Response({'detail':'Email verified successfully!'})
        except UserProfile.DoesNotExist:
            return Response({'detail':'Invalid token'},status=status.HTTP_400_BAD_REQUEST)
        

    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = serializers.PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Password reset link sent (check console in dev mode)")
    
class PasswordResetView(generics.GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Reset Password Successfully")