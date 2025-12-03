from rest_framework import serializers 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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