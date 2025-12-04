from rest_framework import serializers
from .models import Subscription


class SubscriptionSerializers(serializers.ModelSerializer):
    """
    Handle suscription
    """
    class Meta:
        model = Subscription
        fields = ('user', 'plan', 'active')
        read_only_fields = ('user', 'active')

        