from django.shortcuts import render

from rest_framework import viewsets, permissions

from .models import Organization, Team, TeamMembership
from .serializers import OrganizationSerializer, TeamSerializer, TeamMembershipSerializer



class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class TeamMembershipViewSet(viewsets.ModelViewSet):
    serializer_class = TeamMembershipSerializer
    queryset = TeamMembership.objects.all()
    permission_classes = [permissions.IsAuthenticated]
