from rest_framework import serializers # type: ignore
from . import models

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
    