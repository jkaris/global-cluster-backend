from rest_framework import serializers
from .models import Product, SupportTicket, UserRanking


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """

    class Meta:
        """
        Meta class for the Product model.
        """

        model = Product
        fields = "__all__"
        read_only_fields = ("company",)

    def validate(self, data):
        """
        Validates the data provided in the request.
        """
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.user_type not in ["company", "admin"]:
                raise serializers.ValidationError(
                    "Only companies or admins can create products."
                )
            # Set the company here, before validation
            if user.user_type == "company":
                data["company"] = user.companyprofile
            elif user.user_type == "admin":
                # For admin, you might want to require them to specify a company
                if "company" not in data:
                    raise serializers.ValidationError("Admin must specify a company.")
        return data

    def create(self, validated_data):
        """
        Create and return a new `Product` instance, given the validated data.
        """
        # The company should already be in validated_data from the validate method
        return super().create(validated_data)


class SupportTicketSerializer(serializers.ModelSerializer):
    """
    Serializer for the SupportTicket model.
    """

    class Meta:
        """
        Meta class for the SupportTicket model.
        """

        model = SupportTicket
        fields = "__all__"
        read_only_fields = (
            "submitted_by",
        )  # Make submitted_by read-only in the serializer

    def validate(self, data):
        """
        Validates the data provided in the request.
        """
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.user_type not in ["individual", "company"]:
                raise serializers.ValidationError(
                    "Only individuals or companies can create support tickets."
                )
            # Set the submitted_by field here, before validation
            data["submitted_by"] = user
        return data

    def create(self, validated_data):
        """
        Create and return a new `SupportTicket` instance, given the validated data.
        """
        # The submitted_by should already be in validated_data from the validate method
        return super().create(validated_data)


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
