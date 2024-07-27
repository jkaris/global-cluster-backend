from rest_framework import viewsets
from .models import IndividualProfile, CompanyProfile
from .serializers import IndividualProfileSerializer, CompanyProfileSerializer


class IndividualProfileViewSet(viewsets.ModelViewSet):
    queryset = IndividualProfile.objects.all()
    serializer_class = IndividualProfileSerializer


class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
