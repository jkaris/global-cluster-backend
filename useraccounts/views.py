from rest_framework import viewsets, generics, permissions
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import IndividualProfile, CompanyProfile
from .serializers import (
    IndividualProfileSerializer,
    CompanyProfileSerializer,
    CustomUserTokenObtainPairSerializer,
    SignupSerializer,
)


class SignupView(generics.CreateAPIView):
    """
    API endpoint that allows users to signup.
    """

    serializer_class = SignupSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        response_data = {
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
            "user_type": user.user_type,
            "phone_number": user.phone_number,
            "address": user.address,
            "country": user.country,
            "state": user.state,
            "city": user.city,
            "date_joined": user.date_joined,
            "status": user.status,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        if user.user_type == "individual":
            profile = IndividualProfile.objects.get(user=user)
            response_data.update(
                {
                    "gender": profile.gender,
                }
            )
        elif user.user_type == "company":
            profile = CompanyProfile.objects.get(user=user)
            response_data.update(
                {
                    "company_registration_number": profile.company_registration_number,
                }
            )

        return Response(response_data, status=status.HTTP_201_CREATED)


class IndividualProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = IndividualProfile.objects.all()
    serializer_class = IndividualProfileSerializer

    def create(self, request, *args, **kwargs):
        """
        Create and return a new `IndividualProfile` instance, given the validated data.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Include the user_id in the response
        response_data = serializer.data
        response_data["user_id"] = serializer.instance.user.id
        response_data["email"] = serializer.instance.user.email
        response_data["created_at"] = serializer.instance.date_joined
        response_data["status"] = serializer.instance.status

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == "admin" or user.user_type == "company":
            return CompanyProfile.objects.all()
        return CompanyProfile.objects.filter(user=user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # def get_queryset(self):
    #     return CompanyProfile.objects.filter(user=self.request.user)
    #
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #
    #     user = serializer.instance.user
    #     refresh = RefreshToken.for_user(user)
    #     access = refresh.access_token
    #
    #     response_data = serializer.data
    #     response_data.update({
    #         "name": user.name,
    #         "user_id": user.id,
    #         "email": user.email,
    #         "created_at": user.date_joined,
    #         "status": user.status,
    #         "user_type": user.user_type,
    #         "refresh": str(refresh),
    #         "access": str(access)
    #     })
    #
    #     return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data.update({
            "name": instance.user.name,
            "user_id": instance.user.id,
            "email": instance.user.email,
            "created_at": instance.user.date_joined,
            "status": instance.user.status,
            "user_type": instance.user.user_type
        })
        return Response(data)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView
    """

    serializer_class = CustomUserTokenObtainPairSerializer
