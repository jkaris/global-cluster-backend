from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    groups = models.ManyToManyField(
        Group,
        related_name='referrals_user_set',  # Custom related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='referrals_user_set',  # Custom related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

class Referral(models.Model):
    referrer = models.ForeignKey(User, related_name='referrals', on_delete=models.CASCADE)
    referred = models.OneToOneField(User, related_name='referred_user', on_delete=models.CASCADE)
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, default=30.00)
    created_at = models.DateTimeField(auto_now_add=True)
