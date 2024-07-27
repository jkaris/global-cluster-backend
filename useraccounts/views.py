from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import IndividualProfile, CompanyProfile
from .serializers import IndividualProfileSerializer, CompanyProfileSerializer, CustomUserTokenObtainPairSerializer


class IndividualProfileViewSet(viewsets.ModelViewSet):
    queryset = IndividualProfile.objects.all()
    serializer_class = IndividualProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Include the user_id in the response
        response_data = serializer.data
        response_data['user_id'] = serializer.instance.user.id
        response_data['email'] = serializer.instance.user.email
        response_data["created_at"] = serializer.instance.date_joined
        response_data["status"] = serializer.instance.status

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Include the user_id in the response
        response_data = serializer.data
        response_data['user_id'] = serializer.instance.user.id
        response_data['email'] = serializer.instance.user.email
        response_data["created_at"] = serializer.instance.date_joined
        response_data["status"] = serializer.instance.status

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomUserTokenObtainPairSerializer
