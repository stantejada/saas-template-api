from django.db import models
from django.conf import settings


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_organizations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Team(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='teams'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='TeamMembership'
    )

    def __str__(self):
        return f"{self.name} ({self.organization.name})"
    

class TeamMembership(models.Model):
    ROLE_CHOICE = (
        ('owner','Owner'),
        ('admin','Admin'),
        ('member','Member')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICE, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together  = ('user', 'team')
