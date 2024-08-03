from rest_framework import serializers
from .models import Product, SupportTicket, UserRanking, Staff
from useraccounts.models import CustomUser


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
            if user.user_type not in ["individual", "company", "admin"]:
                raise serializers.ValidationError(
                    "Only admins, individuals or companies can create support tickets."
                )
            if self.instance is None:
                data["company"] = user
        return data


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
        read_only_fields = ("submitted_by",)

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
            data["submitted_by"] = user
        return data

    def create(self, validated_data):
        """
        Create and return a new `SupportTicket` instance, given the validated data.
        """
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


class StaffSerializer(serializers.ModelSerializer):
    """
    Serializer for the Staff model.
    """

    email = serializers.EmailField(source="user.email", read_only=True)
    name = serializers.CharField(source="user.name")
    phone_number = serializers.CharField(source="user.phone_number")

    class Meta:
        model = Staff
        fields = [
            "id",
            "email",
            "name",
            "phone_number",
            "role",
            "is_active",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """
        Create a new staff member with the provided validated data.

        Args:
            validated_data (dict): A dictionary containing the validated data for creating a staff member.
                The dictionary should include the following keys:
                - user (dict): A dictionary containing the user data for creating a user.
                    The dictionary should include the following keys:
                    - email (str): The email address of the user.
                    - password (str): The password for the user.

        Returns:
            Staff: The newly created staff member.

        Raises:
            None.
        """
        user_data = validated_data.pop("user")
        email = self.context["request"].data.get("email")
        password = self.context["request"].data.get(
            "password"
        )  # Get password from request data

        user = CustomUser.objects.create_user(
            email=email, password=password, user_type="admin"
        )

        staff = Staff.objects.create(user=user, **validated_data)

        if staff.role == "superadmin":
            user.is_superuser = True
            user.is_staff = True
        elif staff.role == "admin":
            user.is_staff = True
        user.save()

        return staff

    def update(self, instance, validated_data):
        """
        Update the user data of an instance and save the changes.

        Args:
            instance (Staff): The instance to update.
            validated_data (dict): The validated data containing the user data to update.

        Returns:
            Staff: The updated instance.

        Description:
            This function updates the user data of an instance by iterating over the validated_data dictionary
            and updating the corresponding attributes of the instance's user object. The changes are then saved
            by calling the save method of the user object. Finally, the update method of the parent class is called
            with the instance and the validated_data to further update the instance.

            If the 'user' key is not present in the validated_data dictionary, the function does nothing.

            Note: This function assumes that the instance parameter is an instance of the Staff model and that
            the user attribute of the instance is an instance of the CustomUser model.
        """
        user_data = validated_data.pop("user", {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        return super().update(instance, validated_data)
