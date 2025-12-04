from django.shortcuts import render

from rest_framework import viewsets, permissions

from .models import Organization, Team, TeamMembership, Subscription
from .serializers import OrganizationSerializer, TeamSerializer, TeamMembershipSerializer, SubscriptionSerializer

from .permissions import (
    IsOrganizationOwner,
    IsTeamAdminOrOwner,
    IsMember
)

class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOrganizationOwner()]
        return [permissions.IsAuthenticated()]

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeamAdminOrOwner]
        return [permissions.IsAuthenticated(), IsMember()]
    
    def get_queryset(self):
        return Team.objects.filter(organization_in=self.request.user.owned_organizations.all())
    
    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.owned_organizations.first())
    


class TeamMembershipViewSet(viewsets.ModelViewSet):
    serializer_class = TeamMembershipSerializer
    queryset = TeamMembership.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeamAdminOrOwner()]
        return [permissions.IsAuthenticated(), IsMember()]
    
    def get_queryset(self):
        return TeamMembership.objects.filter(organization_in=self.request.user.owned_organizations.all())


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(
            organization_in = self.request.user.owned_organizations.all()
        )