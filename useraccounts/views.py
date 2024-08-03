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
                    "state": profile.state,
                    "city": profile.city,
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


class CompanyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CompanyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return CompanyProfile.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


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
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer

    def create(self, request, *args, **kwargs):
        """
        Create and return a new `CompanyProfile` instance, given the validated data.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Generate tokens
        user = serializer.instance.user
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Include the user_id in the response
        response_data = serializer.data
        response_data["user_id"] = serializer.instance.user.id
        response_data["email"] = serializer.instance.user.email
        response_data["created_at"] = serializer.instance.date_joined
        response_data["status"] = serializer.instance.status
        response_data["refresh"] = str(refresh)
        response_data["access"] = str(access)

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView
    """

    serializer_class = CustomUserTokenObtainPairSerializer
