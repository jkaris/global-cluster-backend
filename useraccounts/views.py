from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import IndividualProfile, CompanyProfile
from .serializers import IndividualProfileSerializer, CompanyProfileSerializer, CustomUserTokenObtainPairSerializer


class IndividualProfileViewSet(viewsets.ModelViewSet):
    queryset = IndividualProfile.objects.all()
    serializer_class = IndividualProfileSerializer


class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomUserTokenObtainPairSerializer
