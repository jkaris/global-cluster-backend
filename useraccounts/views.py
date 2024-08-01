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
        """
        Create and return a new `User` instance, given the validated data.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        response_data = {
            "user_id": user.id,
            "email": user.email,
            "user_type": user.user_type,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        if user.user_type == "individual":
            profile = IndividualProfile.objects.get(user=user)
            response_data.update(
                {
                    "first_name": profile.first_name,
                    "last_name": profile.last_name,
                    "gender": profile.gender,
                    "phone_number": profile.phone_number,
                    "address": profile.address,
                    "country": profile.country,
                    "state": profile.state,
                    "city": profile.city,
                }
            )
        elif user.user_type == "company":
            profile = CompanyProfile.objects.get(user=user)
            response_data.update(
                {
                    "company_name": profile.company_name,
                    "company_registration_number": profile.company_registration_number,
                    "phone_number": profile.phone_number,
                    "address": profile.address,
                    "country": profile.country,
                }
            )

        return Response(response_data, status=status.HTTP_201_CREATED)


class CompanyProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = CompanyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieves the `CompanyProfile` object associated with the currently authenticated user.

        Returns:
            CompanyProfile: The `CompanyProfile` object corresponding to the authenticated user.

        Raises:
            CompanyProfile.DoesNotExist: If no `CompanyProfile` object is found for the authenticated user.
        """
        return CompanyProfile.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        Retrieves the `profile` object associated with the currently authenticated user and serializes it.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized `profile` object.
        """
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Update a company profile with the provided data.

        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized updated company profile.

        Raises:
            ValidationError: If the serializer is not valid.

        Description:
            This function retrieves the company profile associated with the currently authenticated user,
            updates it with the provided data using a serializer, and returns the serialized updated profile.
            The user_id of the authenticated user is also included in the response.
        """
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)
        # Include the user_id in the response
        response_data = serializer.data
        response_data["user_id"] = serializer.instance.user.id
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """
        Updates a partial profile with the provided data.

        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized updated profile.

        Raises:
            ValidationError: If the serializer is not valid.

        Description:
            This function retrieves the profile associated with the currently authenticated user,
            updates it with the provided data using a serializer, and returns the serialized updated profile.
            The profile is updated partially, meaning only the provided fields are updated.
        """
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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
