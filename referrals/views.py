import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, SupportTicket, UserRanking
from .serializers import (
    ProductSerializer,
    SupportTicketSerializer,
    UserRankingSerializer,
    VerifyAccountSerializer,
)
from .permissions import IsCompanyOrAdmin


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Product model.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsCompanyOrAdmin]

    def get_permissions(self):
        """
        Determine the appropriate permissions for the current view action.

        Returns:
            list: A list of permission instances based on the current view action.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsCompanyOrAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Save a new product instance using the provided serializer.

        Args:
            serializer (Serializer): The serializer instance containing the product data.

        Raises:
            PermissionDenied: If the user is not a company or admin.

        Returns:
            None
        """
        if self.request.user.user_type not in ["company", "admin"]:
            raise PermissionDenied("You do not have permission to create a product.")
        serializer.save(company=self.request.user.companyprofile)

    def perform_update(self, serializer):
        """
        Save the updated product instance using the provided serializer.

        Args:
            serializer (Serializer): The serializer instance containing the updated product data.

        Raises:
            PermissionDenied: If the user is not a company or admin.

        Returns:
            None
        """
        if self.request.user.user_type not in ["company", "admin"]:
            raise PermissionDenied("You do not have permission to update a product.")
        serializer.save()


class SupportTicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the SupportTicket model.
    """

    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the support tickets
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return SupportTicket.objects.all()
        return SupportTicket.objects.filter(submitted_by=user)


class UserRankingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the UserRanking model.
    """

    queryset = UserRanking.objects.all()
    serializer_class = UserRankingSerializer
    permission_classes = [IsAuthenticated]


class VerifyAccountView(GenericAPIView):
    """
    View for verifying an account.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = VerifyAccountSerializer

    def get(self, request):
        """
        Retrieves account information from an external API based on the provided account number and bank code.
        """
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        account_number = serializer.validated_data.get("account_number")
        bank_code = serializer.validated_data.get("bank_code")

        # Replace with your actual Bearer token and API URL
        headers = {
            "Authorization": "Bearer Your_Bearer_Token",
        }

        params = {
            "account_number": account_number,
            "bank_code": bank_code,
        }

        try:
            response = requests.get(
                "http://nubapi.test/api/verify", headers=headers, params=params
            )
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()

            return Response(
                {
                    "account_name": data["account_name"],
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "other_name": data["other_name"],
                    "account_number": data["account_number"],
                    "bank_code": data["bank_code"],
                    "bank_name": data["Bank_name"],
                }
            )
        except requests.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
