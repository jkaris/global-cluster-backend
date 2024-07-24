from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from ..models import Company, Individual
from .serializers import CompanySerializer, IndividualSerializer, LoginSerializer


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                if isinstance(user, Company):
                    user_type = "company"
                elif isinstance(user, Individual):
                    user_type = "individual"
                elif user.is_staff:  # Assuming admin users are staff members
                    user_type = "admin"
                else:
                    user_type = "unknown"
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user_id": user.pk,
                        "email": user.email,
                        "user_type": user_type,
                    }
                )
            else:
                return Response(
                    {"detail": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class IndividualCreateView(generics.CreateAPIView):
    queryset = Individual.objects.all()
    serializer_class = IndividualSerializer
