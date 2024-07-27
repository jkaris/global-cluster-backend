from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsCompanyOrAdmin


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsCompanyOrAdmin]

    def perform_create(self, serializer):
        if self.request.user.user_type not in ['company', 'admin']:
            raise PermissionDenied("You do not have permission to create a product.")
        serializer.save(company=self.request.user.companyprofile)

    def perform_update(self, serializer):
        if self.request.user.user_type not in ['company', 'admin']:
            raise PermissionDenied("You do not have permission to update a product.")
        serializer.save()
