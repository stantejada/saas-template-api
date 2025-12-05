from django.shortcuts import render

from rest_framework import viewsets, permissions

from .models import Organization, Team, TeamMembership, Subscription
from .serializers import (
    OrganizationSerializer,
    TeamSerializer,
    TeamMembershipSerializer,
    SubscriptionSerializer
)

from .permissions import (
    IsOrganizationOwner,
    IsTeamAdminOrOwner,
    IsMember
)

from audit.utils import create_audit_log


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        org = serializer.save(owner=self.request.user)
        create_audit_log(
            user=self.request.user,
            organization=org,
            action="organization_created",
            metadata={"name": org.name},
            request=self.request
        )

    def perform_update(self, serializer):
        org = serializer.save()
        create_audit_log(
            user=self.request.user,
            organization=org,
            action="organization_updated",
            metadata={"name": org.name},
            request=self.request
        )

    def perform_destroy(self, instance):
        create_audit_log(
            user=self.request.user,
            organization=instance,
            action="organization_deleted",
            metadata={"name": instance.name},
            request=self.request
        )
        instance.delete()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOrganizationOwner()]
        return [permissions.IsAuthenticated()]


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Team.objects.filter(
            organization__in=self.request.user.owned_organizations.all()
        )

    def perform_create(self, serializer):
        team = serializer.save()
        create_audit_log(
            user=self.request.user,
            organization=team.organization,
            team=team,
            action="team_created",
            metadata={"team_name": team.name},
            request=self.request
        )

    def perform_update(self, serializer):
        team = serializer.save()
        create_audit_log(
            user=self.request.user,
            organization=team.organization,
            team=team,
            action="team_updated",
            metadata={"team_name": team.name},
            request=self.request
        )

    def perform_destroy(self, instance):
        create_audit_log(
            user=self.request.user,
            organization=instance.organization,
            team=instance,
            action="team_deleted",
            metadata={"team_name": instance.name},
            request=self.request
        )
        instance.delete()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeamAdminOrOwner()]
        return [permissions.IsAuthenticated(), IsMember()]


class TeamMembershipViewSet(viewsets.ModelViewSet):
    serializer_class = TeamMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TeamMembership.objects.filter(
            team__organization__in=self.request.user.owned_organizations.all()
        )

    def perform_create(self, serializer):
        membership = serializer.save()
        create_audit_log(
            user=self.request.user,
            organization=membership.team.organization,
            team=membership.team,
            action="member_added",
            metadata={"member_id": membership.user.id, "role": membership.role},
            request=self.request
        )

    def perform_destroy(self, instance):
        create_audit_log(
            user=self.request.user,
            organization=instance.team.organization,
            team=instance.team,
            action="member_removed",
            metadata={"member_id": instance.user.id},
            request=self.request
        )
        instance.delete()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeamAdminOrOwner()]
        return [permissions.IsAuthenticated(), IsMember()]


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(
            organization__in=self.request.user.owned_organizations.all()
        )
