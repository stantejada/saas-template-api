from rest_framework.permissions import BasePermission
from .models import TeamMembership


class IsOrganizationOwner(BasePermission):
    """
    Only organization owner can update/delete the organization,
    Anyone can create their own organization
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
class IsTeamAdminOrOwner(BasePermission):
    """
    Owners/Admins can modify teams and memberships and
    Member can only read
    """

    def has_object_permission(self, request, view, obj):
        team = obj if hasattr(obj, 'organization') else obj.team

        membership = TeamMembership.objects.filter(
            team=team,
            user=request.user
        ).first()

        if membership is None:
            return False
        
        return membership.role in ['owner', 'admin']

class IsMember(BasePermission):
    """
    User should be a member to view team data
    """
    def has_object_permission(self, request, view, obj):
        team = obj if hasattr(obj, 'organization') else obj.team

        return TeamMembership.objects.filter(
            team=team,
            user = request.user
        ).exists()
    

