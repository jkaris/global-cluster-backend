from rest_framework import serializers
from .models import Product, SupportTicket, UserRanking


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """

    class Meta:
        model = Product
        fields = "__all__"

    def validate(self, data):
        """
        Validates the data provided in the request.

        This function checks if the request has a user attribute and if the user's user_type is either 'company' or
        'admin'. If not, it raises a serializers.ValidationError with the message "Only companies or admins can create
        products."

        Parameters:
            data (dict): The data to be validated.

        Returns:
            dict: The validated data.
        """
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.user_type not in ["company", "admin"]:
                raise serializers.ValidationError(
                    "Only companies or admins can create products."
                )
        return data


class SupportTicketSerializer(serializers.ModelSerializer):
    """
    Serializer for the SupportTicket model.
    """

    class Meta:
        model = SupportTicket
        fields = "__all__"

    def validate(self, data):
        """
        Validates the given data for creating a support ticket.

        Args:
            data (dict): The data to be validated.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the user is not an individual or a company.
        """
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.user_type not in ["individual", "company"]:
                raise serializers.ValidationError(
                    "Only individuals or companies can create support tickets."
                )
        return data


class UserRankingSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserRanking model.
    """

    class Meta:
        """
        Meta class for the UserRankingSerializer.
        """

        model = UserRanking
        fields = "__all__"


class VerifyAccountSerializer(serializers.Serializer):
    """
    Serializer for verifying an account.
    """

    account_number = serializers.CharField(max_length=20)
    bank_code = serializers.CharField(max_length=10)
    account_name = serializers.CharField(max_length=255, read_only=True)
    first_name = serializers.CharField(max_length=255, read_only=True)
    last_name = serializers.CharField(max_length=255, read_only=True)
    other_name = serializers.CharField(max_length=255, read_only=True)
    bank_name = serializers.CharField(max_length=255, read_only=True)
