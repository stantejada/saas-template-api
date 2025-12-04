from rest_framework import serializers 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from datetime import timedelta

from . import models
import uuid

class UserProfileSerializer(serializers.ModelSerializer):
    "Serializer for UserProfile model"

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password' : {
                'write_only':True,
                'style':{'input_type':'password'}
            }
        }
    
    def create(self, validated_data):
        """
        Create new user with encrypted password
        """
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )

        return user
    
    def update(self, instance, validated_data):
        """Update user and handle password hashing"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    """ Serializers for registering new users"""

    password = serializers.CharField(write_only = True, min_length=8)

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')

    def create(self, validated_data):
        user = models.UserProfile(
            email=validated_data['email'],
            name = validated_data['name'],
            is_verified = False,
            verification_token = str(uuid.uuid4())
        )
        user.set_password(validated_data['password'])
        user.verification_token = str(uuid.uuid4())
        user.save()
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_verified:
            raise serializers.ValidationError(
                {"detail":"Email not verified"},
                code="Authorization")

        return data
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = models.UserProfile.objects.get(email=value)
        except models.UserProfile.DoesNotExist:
            raise serializers.ValidationError({'detail':'User with this email doesnt exist!'})
        return value
    
    def save(self):
        email = self.validated_data['email']
        user = models.UserProfile.objects.get(email=email)
        token = str(uuid.uuid4())
        user.password_reset_token = token
        user.password_reset_token_expiry = timezone.now() + timedelta(hours=1)
        user.save()

        #Add script for sending a email with link + token
        print(f"===== PASSWORD RESET LINK =====")
        print(f"http://127.0.0.1:8000/api/auth/reset-password/?token={user.password_reset_token}")
        print(f"===============================")
        return user

class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate(self, data):
        try:
            user = models.UserProfile.objects.get(password_reset_token=data['token'])
        except models.UserProfile.DoesNotExist:
            raise serializers.ValidationError('Invalid Token')
        if user.password_reset_token_expiry < timezone.now():
            raise serializers.ValidationError("Token expired!")
        
        data['user']=user
        return data
    
    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.password_reset_token = None
        user.password_reset_token_expiry = None
        user.save()
        return user