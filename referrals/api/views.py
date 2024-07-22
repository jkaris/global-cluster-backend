from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from ..models import User, Referral
from .serializers import UserSerializer, ReferralSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        referred_by_id = request.data.get('referred_by')
        with transaction.atomic():
            user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
                referred_by_id=referred_by_id
            )
            if referred_by_id:
                referrer = User.objects.get(id=referred_by_id)
                referral = Referral.objects.create(referrer=referrer, referred=user)
                referrer.balance += referral.reward_amount
                referrer.save()
        
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
