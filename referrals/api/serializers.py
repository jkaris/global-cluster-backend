from rest_framework import serializers
from ..models import User, Referral

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'referred_by', 'balance']

class ReferralSerializer(serializers.ModelSerializer):
    referrer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    referred = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Referral
        fields = ['id', 'referrer', 'referred', 'reward_amount', 'created_at']
