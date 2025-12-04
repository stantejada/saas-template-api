from rest_framework import serializers
from .models import Organization, Team, TeamMembership, Subscription


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'owner', 'created_at']
        read_only_fields = ['owner', 'created_at']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'organization']

class TeamMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembership
        fields = ['id', 'user', 'team', 'role', 'joined_at']
        read_only_fields = ['joined_at']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'organization', 'plan', 'active']
        read_only_fields = ['user', 'organization', 'active']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['organization'] = self.context['request'].organization
        return super().create(validated_data)