from rest_framework import viewsets, permissions
from .models import AuditLog
from .serializers import AuditLogSerializer
from organizations.models import Organization, Team, TeamMembership



class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        owned_orgs = Organization.objects.filter(
            owner=user
        ).values_list("id", flat=True)

        member_orgs = Organization.objects.filter(
            teams__teammembership__user=user
        ).values_list("id", flat=True)

        from itertools import chain
        org_ids = list(chain(owned_orgs, member_orgs))

        return AuditLog.objects.filter(
            organization_id__in=org_ids
        ).distinct()

    
