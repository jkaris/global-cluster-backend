from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from ..models import Company, Individual, Product, SupportTicket, UserRanking, UserRegistration, BusinessRegistration
from .serializers import (
    CompanySerializer,
    IndividualSerializer,
    LoginSerializer,
    ProductSerializer,
    SupportTicketSerializer,
    UserRankingSerializer,
    UserRegistrationSerializer, BusinessRegistrationSerializer, UserDetailSerializer
)
from django.shortcuts import get_object_or_404
import requests


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                user_serializer = UserDetailSerializer(user)
                response_data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": user_serializer.data
                }
                return Response(response_data)
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


class ProductListCreateAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SupportTicketViewSet(viewsets.ModelViewSet):
    # queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    # http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all the tickets
        for the currently authenticated user.
        """
        user = self.request.user
        return SupportTicket.objects.filter(submitted_by=user)


class UserRankingViewSet(viewsets.ModelViewSet):
    queryset = UserRanking.objects.all()
    serializer_class = UserRankingSerializer


class VerifyAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        account_number = request.query_params.get('account_number')
        bank_code = request.query_params.get('bank_code')

        if not account_number or not bank_code:
            return Response({"error": "Both account_number and bank_code are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Replace with your actual Bearer token and API URL
        headers = {
            'Authorization': 'Bearer Your_Bearer_Token',
        }

        params = {
            'account_number': account_number,
            'bank_code': bank_code,
        }

        try:
            response = requests.get('http://nubapi.test/api/verify', headers=headers, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()

            return Response({
                "account_name": data['account_name'],
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "other_name": data['other_name'],
                "account_number": data['account_number'],
                "bank_code": data['bank_code'],
                "bank_name": data['Bank_name']
            })
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRegistrationView(generics.CreateAPIView):
    queryset = UserRegistration.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "User registered successfully. Awaiting approval."},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BusinessRegistrationView(generics.CreateAPIView):
    queryset = BusinessRegistration.objects.all()
    serializer_class = BusinessRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Business registered successfully. Awaiting approval."},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
