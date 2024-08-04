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

    email = serializers.EmailField(source="user.email", read_only=True)
    name = serializers.CharField(source="user.name", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number")
    address = serializers.CharField(source="user.address")
    country = serializers.CharField(source="user.country")
    status = serializers.CharField(source="user.status", read_only=True)
    user_type = serializers.CharField(source="user.user_type", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        IndividualProfile.objects.create(user=user, **validated_data)
        return user

    class Meta:
        """
        Meta class for IndividualProfileSerializer
        """

        model = IndividualProfile
        fields = [
            "user",
            "gender",
            "email",
            "name",
            "phone_number",
            "address",
            "country",
            "status",
            "user_type",
            "user_id",
        ]


class CompanyProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    name = serializers.CharField(source="user.name", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number")
    address = serializers.CharField(source="user.address")
    country = serializers.CharField(source="user.country")
    status = serializers.CharField(source="user.status", read_only=True)
    user_type = serializers.CharField(source="user.user_type", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = CompanyProfile
        fields = "__all__"
        # fields = [
        #     "email",
        #     "name",
        #     "phone_number",
        #     "address",
        #     "country",
        #     "status",
        #     "user_type",
        #     "user_id",
        #     "company_registration_number",
        # ]


class SignupSerializer(serializers.Serializer):
    """
    Serializer for user signup.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()
    user_type = serializers.ChoiceField(choices=["individual", "company"])
    phone_number = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    country = serializers.CharField(required=False)

    # Fields for individual
    gender = serializers.ChoiceField(choices=["male", "female"], required=False)
    state = serializers.CharField(required=False)
    city = serializers.CharField(required=False)

    # Field for company
    company_registration_number = serializers.CharField(required=False)

    def create(self, validated_data):
        user_fields = [
            "email",
            "password",
            "user_type",
            "name",
            "phone_number",
            "address",
            "country",
        ]
        user_data = {
            field: validated_data.pop(field)
            for field in user_fields
            if field in validated_data
        }

        user = CustomUser.objects.create_user(**user_data)

        if user.user_type == "individual":
            IndividualProfile.objects.create(user=user, **validated_data)
        elif user.user_type == "company":
            CompanyProfile.objects.create(user=user, **validated_data)

        return user

    def validate(self, data):
        user_type = data.get("user_type")

        if user_type == "individual":
            required_fields = ["gender", "state", "city"]
        elif user_type == "company":
            required_fields = ["company_registration_number"]
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
