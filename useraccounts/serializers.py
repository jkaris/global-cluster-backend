from rest_framework import serializers
from .models import CustomUser, IndividualProfile, CompanyProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser
    """

    class Meta:
        model = CustomUser
        fields = ["email", "password", "name", "user_type"]
        extra_kwargs = {"password": {"write_only": True}}


class IndividualProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for IndividualProfile
    """

    class Meta:
        """
        Meta class for IndividualProfileSerializer
        """

        model = IndividualProfile
        fields = [
            "user",
            "gender",
        ]


class CompanyProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for CompanyProfile
    """

    class Meta:
        """
        Meta class for CompanyProfileSerializer
        """

        model = CompanyProfile
        fields = [
            "user",
            "company_registration_number",
        ]


class SignupSerializer(serializers.Serializer):
    """
    Serializer for user signup.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    # name = serializers.CharField()
    user_type = serializers.ChoiceField(choices=["individual", "company"])
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    gender = serializers.ChoiceField(choices=["male", "female"], required=False)
    phone_number = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    company_name = serializers.CharField(required=False)
    company_registration_number = serializers.CharField(required=False)

    def create(self, validated_data):
        """
        Create a new user and their corresponding profile based on the validated data.

        Parameters:
            validated_data (dict): A dictionary containing the validated data for creating a new user and profile.

        Returns:
            CustomUser
        """

        user_fields = ["email", "password", "user_type"]
        user_data = {field: validated_data.pop(field) for field in user_fields}

        user = CustomUser.objects.create_user(**user_data)

        if user.user_type == "individual":
            IndividualProfile.objects.create(user=user, **validated_data)
        elif user.user_type == "company":
            CompanyProfile.objects.create(user=user, **validated_data)

        return user

    def validate(self, data):
        """
        Validate the data provided in the request.
        :param data:
        :return:
        """
        user_type = data.get("user_type")

        if user_type == "individual":
            required_fields = ["first_name", "last_name", "gender"]
        elif user_type == "company":
            required_fields = ["company_name", "company_registration_number"]
        else:
            raise serializers.ValidationError("Invalid user type")

        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(
                    f"{field} is required for {user_type} signup"
                )

        return data


class CustomUserTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for CustomUserTokenObtainPair
    """

    def validate(self, attrs):
        """
        Validate and return the user and access token pair.
        :param attrs:
        :return:
        """
        data = super().validate(attrs)

        user = self.user
        if user.user_type == "individual":
            profile_data = IndividualProfileSerializer(
                IndividualProfile.objects.get(user=user)
            ).data
        elif user.user_type == "company":
            profile_data = CompanyProfileSerializer(
                CompanyProfile.objects.get(user=user)
            ).data
        else:
            profile_data = {}

        data.update(
            {
                "refresh": data.get("refresh"),
                "access": data.get("access"),
                "user": {
                    "user_id": user.id,
                    "email": user.email,
                    "is_active": user.is_active,
                    "user_type": user.user_type,
                    "profile": {**profile_data, "user_id": user.id},
                },
            }
        )

        return data
