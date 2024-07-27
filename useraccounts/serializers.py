from rest_framework import serializers
from .models import CustomUser, IndividualProfile, CompanyProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "name", "user_type", "password", "profile_picture"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class IndividualProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    user_type = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    is_active = serializers.BooleanField(default=True, write_only=True)
    created_at = serializers.DateTimeField(source='user.date_joined', read_only=True)

    class Meta:
        model = IndividualProfile
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "gender",
            "phone_number",
            "address",
            "country",
            "state",
            "city",
            "email",
            "password",
            "user_type",
            "status",
            "is_active",
            "created_at"
        ]

    def create(self, validated_data):
        user_data = {
            "email": validated_data.pop("email"),
            "password": validated_data.pop("password"),
            "user_type": validated_data.pop("user_type"),
            "is_active": validated_data.pop("is_active"),
        }
        user = CustomUser.objects.create_user(**user_data)
        individual_profile = IndividualProfile.objects.create(
            user=user, **validated_data
        )
        return individual_profile

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_id'] = instance.user.id
        representation['status'] = instance.status
        representation['is_active'] = instance.user.is_active
        representation['created_at'] = instance.date_joined
        representation['user_type'] = instance.user.user_type
        representation['email'] = instance.user.email
        return representation

    def update(self, instance, validated_data):
        user_data = {
            "email": validated_data.pop("email", None),
            "password": validated_data.pop("password", None),
            "user_type": validated_data.pop("user_type", None),
            "is_active": validated_data.pop("is_active", instance.user.is_active),
        }
        user = instance.user

        if user_data["email"]:
            user.email = user_data["email"]
        if user_data["password"]:
            user.set_password(user_data["password"])
        if user_data["user_type"]:
            user.user_type = user_data["user_type"]
        user.is_active = user_data["is_active"]

        user.save()
        instance = super().update(instance, validated_data)
        return instance


class CompanyProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    user_type = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(default=True, write_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)  # Add this line
    created_at = serializers.DateTimeField(source='user.date_joined', read_only=True)

    class Meta:
        model = CompanyProfile
        fields = [
            "user_id",
            "company_name",
            "company_registration_number",
            "phone_number",
            "address",
            "country",
            "user_type",
            "email",
            "password",
            "is_active",
            "created_at",
        ]

    def create(self, validated_data):
        user_data = {
            "email": validated_data.pop("email"),
            "password": validated_data.pop("password"),
            "user_type": validated_data.pop("user_type"),
            "is_active": validated_data.pop("is_active"),
        }
        user = CustomUser.objects.create_user(**user_data)
        company_profile = CompanyProfile.objects.create(user=user, **validated_data)
        return company_profile

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_id'] = instance.user.id
        representation['user_type'] = instance.user.user_type
        representation['email'] = instance.user.email
        representation['status'] = instance.status
        representation['is_active'] = instance.user.is_active
        return representation

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user

        serializer = CustomUserSerializer(user, data=user_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        instance = super().update(instance, validated_data)
        return instance


class CustomUserTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        if user.user_type == 'individual':
            profile_data = IndividualProfileSerializer(IndividualProfile.objects.get(user=user)).data
        elif user.user_type == 'company':
            profile_data = CompanyProfileSerializer(CompanyProfile.objects.get(user=user)).data
        else:
            profile_data = {}

        data.update({
            "refresh": data.get("refresh"),
            "access": data.get("access"),
            "user": {
                "email": user.email,
                "is_active": user.is_active,
                "user_type": user.user_type,
                "profile": {
                    **profile_data
                }
            }
        })

        return data

