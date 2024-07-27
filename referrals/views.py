from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, SupportTicket
from .serializers import ProductSerializer, SupportTicketSerializer
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
        if self.action in ['list', 'retrieve']:
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
        if self.request.user.user_type not in ['company', 'admin']:
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
        if self.request.user.user_type not in ['company', 'admin']:
            raise PermissionDenied("You do not have permission to update a product.")
        serializer.save()


class SupportTicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the SupportTicket model.
    """
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.user_type not in ['individual', 'company']:
            raise PermissionDenied("You do not have permission to create a support ticket.")
        serializer.save(submitted_by=self.request.user)
