from django.db import models
from users.models import UserProfile

# Create your models here.
class Subscription(models.Model):
    PLAN_CHOICES = [
        ('free', 'free'),
        ('pro', 'pro'),
        ('enterprise', 'enterprise')
    ]

    user = models.OneToOneField(
        UserProfile, 
        on_delete=models.CASCADE,
        related_name='billing_subscriptions')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan}"
    
