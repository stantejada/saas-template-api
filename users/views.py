from django.shortcuts import render

from rest_framework import viewsets, filters # type: ignore
from rest_framework_simplejwt.authentication import JWTAuthentication # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore


from . import models, serializers
from . import permissions

# Create your views here.

class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handle creating and updating user profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)