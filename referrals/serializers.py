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

    def __init__(self, *args, **kwargs):
        """
        Initializes the serializer instance.

        This method is called when a serializer instance is created. It sets the `required` attribute of all fields to `False` if the request method is either "PUT" or "PATCH".

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
                context (dict, optional): The context of the serializer. Defaults to None.

        Returns:
            None
        """
        super().__init__(*args, **kwargs)
        request = self.context.get("request") if 'context' in kwargs else None
        if request and request.method in ["PUT", "PATCH"]:
            for field in self.fields.values():
                field.required = False

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
                data["company"] = user
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

    def update(self, instance, validated_data):
        """
        Update and return an existing `Product` instance, given the validated data.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


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


class StaffSerializer(serializers.ModelSerializer):
    """
    Serializer for the Staff model.
    """
    email = serializers.EmailField(source='user.email')
    is_active = serializers.BooleanField(source='user.is_active')

    class Meta:
        model = Staff
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'is_active']
        read_only_fields = ['id']

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
        user_data = validated_data.pop('user')
        email = user_data['email']
        password = self.context['request'].data.get('password')  # Get password from request data

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            user_type='admin'
        )

        staff = Staff.objects.create(user=user, **validated_data)

        if staff.role == 'superadmin':
            user.is_superuser = True
            user.is_staff = True
        elif staff.role == 'admin':
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
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        return super().update(instance, validated_data)
