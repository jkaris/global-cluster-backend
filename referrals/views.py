import requests
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Product, SupportTicket, UserRanking, Staff
from .serializers import (
    ProductSerializer,
    SupportTicketSerializer,
    UserRankingSerializer,
    VerifyAccountSerializer,
    StaffSerializer,
)
from .permissions import IsOwnerOrAdmin

logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Product model.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Product.objects.all()
        elif user.user_type == 'company':
            return Product.objects.filter(company=user)
        else:
            return Product.objects.none()

    def update(self, request, *args, **kwargs):
        """
        Update an instance of the model using the provided serializer.
        """
        logger.info(f"Updating product: {request.data}")
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


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


class StaffViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Staff model.
    """

    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Saves the data from the serializer into the database.

        Args:
            serializer (Serializer): The serializer instance containing the data to be saved.

        Returns:
            None
        """
        serializer.save()

    def get_queryset(self):
        """
        Get all Staff objects from the database.

        Returns:
            QuerySet: A queryset containing all Staff objects.
        """
        return Staff.objects.all()
